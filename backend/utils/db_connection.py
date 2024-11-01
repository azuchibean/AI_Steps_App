import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT"),
            ssl_disabled=False
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def create_user_table(connection):
    """Creates the users table if it does not already exist."""
    cursor = connection.cursor()
    try:
        # can specify details of it, probably requires first name, email, hashed password, api key, and number of times api used
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(20) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("User table created")
    except Error as e:
        print("Error creating table", e)
        return None
    finally:
        cursor.close() 

def insert_user(connection, name, email, password):
    """Inserts a new user into the users table."""
    cursor = connection.cursor()
    try:
        # can change for specific requirements
        insert_user_query = """
        INSERT INTO users (name, email, password) VALUES (%s, %s, %s)
        """
        cursor.execute(insert_user_query, (name, email, password))
        connection.commit()
        print("User inserted successfully.")
    except Error as e:
        print("Error inserting user", e)
        connection.rollback()
    finally:
        cursor.close() 

def close_db_connection(connection):
    """Closes the database connection."""
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed")
