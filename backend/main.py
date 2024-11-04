# API server is here
from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from model_handler import llm_test
from utils.models.models import RegisterRequest, LoginRequest, PasswordResetRequest, PasswordReset
from utils.db_connection import get_db_connection, close_db_connection, create_user_table, insert_user, get_user_by_email, update_user_password
from utils.auth_utils import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, RESET_PASSWORD_SECRET_KEY, create_password_reset_token, MAILGUN_API_KEY, MAILGUN_DOMAIN,SENDER_EMAIL
from datetime import timedelta
import requests 

app = FastAPI()

# Configure CORS middleware to allow your frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "*"],  # Temporarily allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the OAuth2PasswordBearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Define the function to retrieve the current user from the token
async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        close_db_connection(db)

    return {"message": "User registered successfully!"}



# Login endpoint
@app.post("/login")
async def login(request: LoginRequest):
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

    return {"access_token": access_token, "token_type": "bearer", "isAdmin": user.get("is_admin") }


# Verify token endpoint
@app.get("/verify-token")
async def verify_token(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Token is valid",
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
    reset_link = f"http://127.0.0.1:5500/reset-password.html?token={token}"  # Replace with your frontend URL
    

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

@app.get("/llm_test")
async def llm_message():
    generated_text = llm_test()
    return {"response": generated_text}

#Creates user table if it doesn't exist
def main():
    db = get_db_connection()
    if db is None:
        print("Failed to connect to database.")
        return

    try:
        create_user_table(db)

    except Error as e:
        print(f"The error '{e}' occurred")

    finally:
        close_db_connection(db) 


if __name__ == "__main__":
    main()
