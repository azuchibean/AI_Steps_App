# API server is here
from fastapi import FastAPI
from utils.db_connection import get_db_connection, close_db_connection, create_user_table, insert_user

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}

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