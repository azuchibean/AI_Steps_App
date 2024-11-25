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
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        is_admin BOOLEAN DEFAULT FALSE
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

def insert_user(connection, first_name, email, password_hash):
    """Inserts a new user into the users table."""
    cursor = connection.cursor()
    try:
        insert_user_query = """
        INSERT INTO users (first_name, email, password_hash) VALUES (%s, %s, %s)
        """
        cursor.execute(insert_user_query, (first_name, email, password_hash))
        connection.commit()
        print("User inserted successfully.")
    except Error as e:
        print("Error inserting user", e)
        connection.rollback()
    finally:
        cursor.close() 

def get_user_by_email(connection, email):
    """Retrieve a user from the database by email."""
    cursor = connection.cursor(dictionary=True)
    try:
        select_query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(select_query, (email,))
        user = cursor.fetchone()
        return user
    except Error as e:
        print("Error retrieving user by email:", e)
        connection.rollback()
        return None
    finally:
        cursor.close()

def update_user_password(connection, email, hashed_password):
    """Updates user password"""
    cursor = connection.cursor()
    try:
        update_query = """
        UPDATE users SET password_hash = %s WHERE email = %s
        """
        cursor.execute(update_query,(hashed_password, email))
        connection.commit()
    except Error as e:
        print("Error updating user password:", e)
        connection.rollback()
    finally:
        cursor.close()

def close_db_connection(connection):
    """Closes the database connection."""
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed")
        
def create_endpoint_table(connection):
    """Creates the endpoints table if it does not already exist."""
    cursor = connection.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS endpoints (
        id INT AUTO_INCREMENT PRIMARY KEY,
        method VARCHAR(10) NOT NULL,
        endpoint VARCHAR(255) NOT NULL,
        count INT DEFAULT 0,
        UNIQUE (method, endpoint)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Endpoints table created")
    except Error as e:
        print("Error creating table", e)
        return None
    finally:
        cursor.close() 

def get_endpoint_stats_from_db(connection):
    """
    Endpoint to get stats for all logged endpoints.
    Returns a list of endpoint statistics.
    """
    try:
        cursor = connection.cursor()
        query = "SELECT method, endpoint, count FROM endpoints"
        cursor.execute(query)
        result = cursor.fetchall()

        # If no data is found, return an empty list
        if not result:
            raise HTTPException(status_code=404, detail="No endpoint stats found")

        # Prepare the response data
        stats = [{"method": row[0], "endpoint": row[1], "count": row[2]} for row in result]

        return stats 
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error fetching endpoint stats: {e}")
    finally:
        cursor.close()
        close_db_connection(connection)
        
def create_api_usage_table(connection):
    """Creates the api usage table if it does not already exist."""
    cursor = connection.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS api_usage (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL UNIQUE,
        total_api_calls INT DEFAULT 0,
        llm_api_calls INT DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Usage table created")
    except Error as e:
        print("Error creating table", e)
        return None
    finally:
        cursor.close() 
        
def initialize_usage_record(connection, user_id):
    """Inserts new user into api usage table"""
    cursor = connection.cursor()
    try:
        insert_query = """
        INSERT INTO api_usage (user_id) VALUES (%s)
        """
        cursor.execute(insert_query, (user_id,))
        connection.commit()
        print(f"Initialized usage record for user_id {user_id}")
    except Error as e:
        print("Error initializing usage record:", e)
        connection.rollback()
    finally:
        cursor.close()

def get_api_usage_data(connection):
    """Fetch API usage data with user details."""
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        SELECT 
            users.first_name, 
            users.email, 
            api_usage.total_api_calls
        FROM 
            api_usage
        JOIN 
            users 
        ON 
            api_usage.user_id = users.id
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print("Error fetching API usage data:", e)
        connection.rollback()
        return []
    finally:
        cursor.close()


def get_api_usage_data_for_user(connection, user_id):
    """Fetch API usage data for a specific user."""
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT * FROM api_usage
            WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        # If results are found
        if results:
            result = results[0]  # Extract the first row
            free_calls_remaining = max(20 - result.get("llm_api_calls", 0), 0)  # Default to 0 if key is missing
            result["warning"] = (
                "You have exceeded your 20 free API calls. Additional requests may incur charges."
                if free_calls_remaining == 0
                else None
            )
            result["free_calls_remaining"] = free_calls_remaining
            return result

        # If no results are found, return a default structure
        return {
            "llm_api_calls": 0,
            "free_calls_remaining": 20,
            "warning": None
        }
    except Error as e:
        connection.rollback()
        print("Error fetching API usage data for user:", e)
        return {
            "llm_api_calls": 0,
            "free_calls_remaining": 20,
            "warning": "Error fetching API usage data. Please try again later."
        }
    finally:
        cursor.close()


def update_user_name(connection, user_id, new_name):
    """
    Updates the user's name in the database.
    """
    cursor = connection.cursor()
    try:
        update_query = "UPDATE users SET first_name = %s WHERE id = %s"
        cursor.execute(update_query, (new_name, user_id))
        connection.commit()
        return True
    except Error as e:
        print(f"Error updating name for user_id {user_id}: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()


def delete_user(connection, user_id):
    """Deletes a user from the database."""
    cursor = connection.cursor()
    try:
        delete_query = """
        DELETE FROM users WHERE id = %s
        """
        cursor.execute(delete_query, (user_id,))
        connection.commit()
        return True
    except Error as e:
        print("Error deleting user:", e)
        connection.rollback()
        return False
    finally:
        cursor.close()
