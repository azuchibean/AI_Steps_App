from fastapi import Request
from utils.db_connection import get_db_connection, close_db_connection

async def log_endpoint_stats(request: Request):
    """
    Middleware to log each API request into the `endpoints` table.
    """
    method = request.method
    path = request.url.path

    # Skip logging for certain paths (e.g., static files, favicon, etc.)
    if path.startswith("/static") or path == "/favicon.ico" or request.method == "OPTIONS":
        return 

    # Log the request in the database
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO endpoints (method, endpoint, count)
        VALUES (%s, %s, 1)
        ON DUPLICATE KEY UPDATE count = count + 1
        """
        cursor.execute(query, (method, path))
        connection.commit()
    except Exception as e:
        print(f"Error logging request to database: {e}")
    finally:
        cursor.close()
        close_db_connection(connection)


async def update_user_api_usage(user_id):
    """
    Updates the user's API usage in the `api_usage` table by increasing `total_api_calls`.
    """

    connection = get_db_connection()
    try:
        cursor = connection.cursor()

        # Update the `api_usage` table for the specific user
        query = """
        INSERT INTO api_usage (user_id, total_api_calls)
        VALUES (%s, 1)  
        ON DUPLICATE KEY UPDATE total_api_calls = total_api_calls + 1
        """
        cursor.execute(query, (user_id,))
        connection.commit()

    except Exception as e:
        print(f"Error updating `api_usage` table: {e}")
    finally:
        cursor.close()
        close_db_connection(connection)

async def update_llm_api_calls(user_id:int):
    """Update the llm_api_calls for a user in the api_usage table"""
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        update_query = """
        UPDATE api_usage 
        SET llm_api_calls = llm_api_calls + 1
        WHERE user_id = %s
        """
        cursor.execute(update_query, (user_id,))
        connection.commit()
        print(f"LLM API calls updated for user_id {user_id}")
    except Error as e:
        print("Error updating LLM API calls:", e)
        connection.rollback()
    finally:
        cursor.close()

