# API server is here
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from utils.db_connection import get_db_connection, close_db_connection, create_user_table, insert_user, get_user_by_email
from utils.auth_utils import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from pydantic import BaseModel
from datetime import timedelta
import bcrypt


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



@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}



# Register endpoint
class RegisterRequest(BaseModel):
    first_name: str
    email: str
    password: str

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
class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(request: LoginRequest):
    # Connect to the database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")

    # Retrieve the user by email
    user = get_user_by_email(db, request.email)
    close_db_connection(db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(request.password, user["password_hash"]):
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

    return {"access_token": access_token, "token_type": "bearer"}





#db is tested here, will be put in api not in main later
def main():
    db = get_db_connection()
    if db is None:
        print("Failed to connect to database.")
        return

    try:
        # Create a cursor and execute queries
        create_user_table(db)

        # Note: Enclose string values in quotes
        insert_user(db, "Victor", "victors@gmail.com", "testpass")

    except Error as e:
        print(f"The error '{e}' occurred")

    finally:
        close_db_connection(db)  # Ensure the database connection is closed


if __name__ == "__main__":
    main()