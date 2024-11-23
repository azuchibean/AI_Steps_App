# API server is here
from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks, Response, Request
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from utils.models.models import LocationDetails, RegisterRequest, LoginRequest, PasswordResetRequest, PasswordReset
from utils.db_connection import get_db_connection, close_db_connection, create_user_table, insert_user, get_user_by_email, update_user_password, create_endpoint_table, get_endpoint_stats_from_db, create_api_usage_table, initialize_usage_record, get_api_usage_data, get_api_usage_data_for_user
from utils.auth_utils import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, RESET_PASSWORD_SECRET_KEY, create_password_reset_token, MAILGUN_API_KEY, MAILGUN_DOMAIN,SENDER_EMAIL
from datetime import timedelta
import requests 
from utils.request_logger import log_endpoint_stats, update_user_api_usage
from model_handler import llm_run

app = FastAPI()

# Configure CORS middleware to allow your frontend origin
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://127.0.0.1:5500","https://isa-project-frontend.netlify.app", "https://isa-frontend-285df755bfe6.herokuapp.com"],  # Temporarily allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# log api call
@app.middleware("http")
async def log_request_and_update_usage(request: Request, call_next):
    """
    Middleware that logs the request to the `endpoints` table
    and updates the user's API usage in the `api_usage` table.
    """
    # Check if the request contains a valid user (auth token)
    user = None
    try:
        user = await get_current_user(request)  
    except HTTPException:
        pass

    if user:
        # If the user is authenticated, proceed with logging and updating usage
        user_id = user["id"]
        
        # Log the request to the `endpoints` table
        await log_endpoint_stats(request)
        
        # Update the user's API usage in the `api_usage` table
        await update_user_api_usage(user_id)

    # Process the request and return the response
    response = await call_next(request)
    return response


# Preflight Handler 
@app.options("/{path:path}")
async def preflight_handler():
    return Response(status_code=200)


# Define the OAuth2PasswordBearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Define the function to retrieve the current user 
async def get_current_user(request: Request):
    
    # Extract the token from the cookie
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided",
        )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")


        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    # Connect to the database and retrieve the user
    db = get_db_connection()
    user = get_user_by_email(db, email)
    close_db_connection(db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to my FastAPI application!"}

# Register endpoint
@app.post("/register")
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



# Login endpoint
@app.post("/login")
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



# Verify token endpoint
@app.get("/verify-token")
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
    
   


def send_reset_email(email: str, reset_link: str):
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Your App <mailgun@{MAILGUN_DOMAIN}>",
            "to": email,
            "subject": "Password Reset Request",
            "text": f"Click the link to reset your password: {reset_link}"
        }
    )
    print(response.status_code, response.text)  # Log the response to check for issues



@app.post("/request-password-reset")
async def request_password_reset(request: PasswordResetRequest, background_tasks: BackgroundTasks):
    # Verify if the email exists in the database
    db = get_db_connection()
    user = get_user_by_email(db, request.email)
    close_db_connection(db)

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate the password reset token
    token = create_password_reset_token(request.email)
    reset_link = f"https://isa-project-frontend.netlify.app/reset-password.html?token={token}"  # Replace with your frontend URL
    

    # Send the email with the reset link (mocked here for demonstration)
    background_tasks.add_task(send_reset_email, user["email"], reset_link)

    return {"message": "Password reset link has been sent to your email"}


@app.post("/reset-password")
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
    update_user_password(db, email, hashed_password)  # Implement this function to update the user's password
    close_db_connection(db)

    return {"message": "Password has been reset successfully"}

# Parameters: latitude, longitude, height of person in cm, steps desired, and location_type
# Supported types: https://developers.google.com/maps/documentation/places/web-service/supported_types
# Returns json with two fields: api_response and llm_response. api_response has three objects, while llm_response is response chosen by llm.
# Add text to highlight the one chosen by llm as "recommended" when display on front-end
@app.post("/llm")
async def llm_start(request: LocationDetails):
    latitude = request.latitude
    longitude = request.longitude
    height = request.height
    steps = request.steps
    location_type = request.location_type

    response = llm_run(latitude, longitude, height, steps, location_type)
    return {"response": response}

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


@app.get("/stats/endpoints")
async def get_endpoint_stats():
    """Endpoint to get the count of all endpoints."""
    # Connect to the database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    result = get_endpoint_stats_from_db(db)
    return result

@app.get("/stats/apiUsage")
async def usage_data():
    """Endpoint to get the api usage of all users."""
    # Connect to the database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    result = get_api_usage_data(db)
    return result 

@app.get("/stats/apiUsage/{user_id}")
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


#Creates tables if it doesn't exist ON START UP
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


if __name__ == "__main__":
    main()
