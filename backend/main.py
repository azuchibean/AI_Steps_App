# API server is here
from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks, Response, Request, Body
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from utils.models.models import LocationDetails, LocationDetailsResponse, RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, LogoutResponse, PasswordResetRequest, PasswordResetRequestResponse, PasswordReset, PasswordResetResponse, VerifyTokenResponse, EndpointStatsListResponse, ApiUsageListResponse, ApiUsageForUserResponse, DeleteAccountResponse, UpdateNameResponse
from utils.db_connection import get_db_connection, close_db_connection, create_user_table, insert_user, get_user_by_email, update_user_password, create_endpoint_table, get_endpoint_stats_from_db, create_api_usage_table, initialize_usage_record, get_api_usage_data, get_api_usage_data_for_user, delete_user, update_user_name
from utils.auth_utils import hash_password, verify_password, create_access_token, create_password_reset_token, send_reset_email, get_current_user
from datetime import timedelta
from utils.request_logger import log_endpoint_stats, update_user_api_usage, update_llm_api_calls
from model_handler import llm_run
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
RESET_PASSWORD_SECRET_KEY = os.getenv("RESET_PASSWORD_SECRET_KEY")

app = FastAPI()

# Configure CORS middleware to allow your frontend origin
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://127.0.0.1:5500", "https://dn3aeuakeqz2h.cloudfront.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logs API calls
@app.middleware("http")
async def log_request_and_update_usage(request: Request, call_next):
    """
    Middleware that logs the request to the `endpoints` table
    and updates the user's API usage in the `api_usage` table.
    """
    
    # Log the request to the `endpoints` table
    await log_endpoint_stats(request)
        
    # Check if the request contains a valid user (auth token)
    user = None
    try:
        user = await get_current_user(request)  
    except HTTPException:
        pass

    if user:
        # If the user is authenticated, proceed with logging and updating usage
        user_id = user["id"]
        
        # Update the user's API usage in the `api_usage` table
        await update_user_api_usage(user_id)
        
        if request.url.path == '/api/v1/llm' and request.method == 'POST':
            await update_llm_api_calls(user_id)
        
    # Process the request and return the response
    response = await call_next(request)
    return response


# Preflight handler 
@app.options("/{path:path}",
    summary="Preflight request handler",
    description="Handles preflight requests for CORS by responding with a 200 status code.")
async def preflight_handler():
    return Response(status_code=200)


# Creates tables on start up if they don't exist
@app.on_event("startup")
async def on_startup():
    db = get_db_connection()
    if db is None:
        print("Failed to connect to database.")
        return

    try:
        create_user_table(db)
        create_endpoint_table(db)
        create_api_usage_table(db)

    except Error as e:
        print(f"The error '{e}' occurred")

    finally:
        close_db_connection(db) 


@app.get(
    "/",
    summary="Root/health check endpoint",
    description="This endpoint serves as a health check to indicate that the application is running. It returns a simple JSON message."
)
async def read_root():
    return {"message": "This response means that the app is running."}


@app.post("/api/v1/register", 
    response_model=RegisterResponse,
    summary="Register a new user", 
    description="This endpoint registers a new user by accepting user details such as first name, email, and password. It checks for an existing user and hashes the password before storing it.")
async def register_user(request: RegisterRequest):
     # Connect to the database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Check if the email already exists
    existing_user = get_user_by_email(db, request.email)
    if existing_user:
        close_db_connection(db)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )
    
    # Hash the password
    hashed_password = hash_password(request.password)

    try:
        # Insert the user into the database
        insert_user(db, request.first_name, request.email, hashed_password)
        
        # Get the user_id of the newly inserted user
        user = get_user_by_email(db, request.email)
        if user:
            user_id = user["id"]
            initialize_usage_record(db, user_id)    # initialize the user in api usage table
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        close_db_connection(db)

    return {"message": "User registered successfully!"}


@app.post("/api/v1/login", 
    response_model=LoginResponse, 
    summary="Login user into application", 
    description="This endpoint authenticates the user and returns a JWT token in a secure HTTP-only cookie.")
async def login(request: LoginRequest, response: Response):
    # Connect to the database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")

    # Retrieve the user by email
    user = get_user_by_email(db, request.email)
    close_db_connection(db)

    # Verify if user exists or if password doesn't match
    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate a JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )

    # Set the token in an HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
        samesite="None",
        path="/"  # Ensure cookie is available for all paths
    )

    return {"message": "Login successful", "isAdmin": user.get("is_admin")}


@app.post("/api/v1/logout", 
    response_model = LogoutResponse,
    summary="Log user out of application",
    description="This endpoint logs out the user by deleting the JWT token from the HTTP-only cookie.")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


@app.post("/api/v1/request-password-reset", 
    response_model = PasswordResetRequestResponse,
    summary="Request a password reset",
    description="This endpoint sends a password reset link to the user's email.")
async def request_password_reset(request: PasswordResetRequest, background_tasks: BackgroundTasks):
    # Verify if the email exists in the database
    db = get_db_connection()
    user = get_user_by_email(db, request.email)
    close_db_connection(db)

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate the password reset token
    token = create_password_reset_token(request.email)
    reset_link = f"https://dn3aeuakeqz2h.cloudfront.net/reset-password.html?token={token}"  # Replace with your frontend URL

    # Send the email with the reset link (mocked here for demonstration)
    background_tasks.add_task(send_reset_email, user["email"], reset_link)

    return {"message": "Password reset link has been sent to your email"}


@app.post("/api/v1/reset-password", 
    response_model = PasswordResetResponse,
    summary="Reset user password",
    description="This endpoint resets the user's password using a valid token and new password.")
async def reset_password(request: PasswordReset):
    try:
        # Decode the token
        payload = jwt.decode(request.token, RESET_PASSWORD_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Connect to the database and update the user's password
    db = get_db_connection()
    user = get_user_by_email(db, email)
    if not user:
        close_db_connection(db)
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = hash_password(request.new_password)
    update_user_password(db, email, hashed_password)
    close_db_connection(db)

    return {"message": "Password has been reset successfully"}

# LLM endpoint
@app.post("/api/v1/llm", response_model=LocationDetailsResponse, 
    summary="Posts user location, details, and desired location type to LLM.", 
    description="This endpoint returns a response that contains a processed Places API response and the LLM's recommendation response.")
async def llm_start(request: LocationDetails):
    latitude = request.latitude
    longitude = request.longitude
    height = request.height
    steps = request.steps
    location_type = request.location_type

    response = llm_run(latitude, longitude, height, steps, location_type) 

    return {"response": response}


# Verify token endpoint
@app.get("/api/v1/verify-token", 
    response_model = VerifyTokenResponse,
    summary="Verify if the token is valid and retrieve user information",
    description="This endpoint verifies the validity of the current user's token and returns related user information.")
async def verify_token(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Token is valid",
        "user_id": current_user["id"],
        "user": current_user["email"],
        "isAdmin": current_user.get("is_admin", 0),  
        "free_api_calls_remaining": current_user.get("free_api_calls_remaining", 0) ,
        "total_api_calls": current_user.get("total_api_calls", 0),
        "first_name": current_user.get("first_name", "")
    }

# Retrieve stats for all API endpoints
@app.get("/api/v1/stats/endpoints",
         response_model=EndpointStatsListResponse,
         summary="Get endpoint usage statistics",
         description="Retrieve statistics for all API endpoints, including HTTP method, endpoint path, and usage count."
        )
async def get_endpoint_stats():
    """Endpoint to get the count of all endpoints."""
    # Connect to the database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    result = get_endpoint_stats_from_db(db)
    return {"endpoints": result}

# Retrieve stats of api usages of all users
@app.get("/api/v1/stats/apiUsage",
         response_model=ApiUsageListResponse,
         summary="Get API usage statistics for all users",
         description="Retrieve statistics for API usage by all users, including their total API calls.",
        )
async def usage_data():
    """Endpoint to get the api usage of all users."""
    # Connect to the database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    result = get_api_usage_data(db)
    return {"users": result} 

# Retrieve stats of api usage from a specific user given the user_id
@app.get("/api/v1/stats/apiUsage/{user_id}",
         response_model=ApiUsageForUserResponse,
         summary="Get API usage statistics for a specific user",
         description="Retrieve the API usage statistics for a specific user by user ID, including total API calls."
        )
async def usage_data_for_user(user_id: int):
    """Endpoint to get the API usage for a specific user."""
    # Connect to the database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")

    result = get_api_usage_data_for_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found or no API usage data available")
    return result

# Updates the user's name 
@app.put("/api/v1/update-name",
         response_model=UpdateNameResponse,
         summary="Updates the user's name in the database",
         description="Allows the user to update their name. The new name should be provided in the request body.")
async def update_name(new_name: str = Body(..., embed=True), current_user: dict = Depends(get_current_user)):
    """
    Updates the user's name in the database.
    """
    user_id = current_user["id"]
    
    # Connect to the database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        # Use the function from db_connection.py to update the name
        success = update_user_name(db, user_id, new_name)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update name")
        
        return {"message": "Name updated successfully"}
    finally:
        close_db_connection(db)

# Deletes the user's account
@app.delete("/api/v1/delete-account",
            response_model=DeleteAccountResponse,
            summary="Deletes the user's account from the database",
            description="Allows the user to permanently delete their account.")
async def delete_account(response: Response, current_user: dict = Depends(get_current_user)):
    # Get the user's ID from the current_user
    user_id = current_user["id"]
    
    # Connect to the database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        # Delete the user
        success = delete_user(db, user_id)
        if success:
            # Delete the access token cookie
            response.delete_cookie("access_token")
            return {"message": "Account deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete account")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_db_connection(db)