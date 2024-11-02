# API server is here
from fastapi import FastAPI, HTTPException
from utils.db_connection import get_db_connection, close_db_connection, create_user_table, insert_user
from pydantic import BaseModel
import bcrypt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS middleware to allow your frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    # Hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), salt)

    # Connect to the database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        # Insert the user into the database
        insert_user(db, request.first_name, request.email, hashed_password.decode('utf-8'))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        close_db_connection(db)

    return {"message": "User registered successfully!"}



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