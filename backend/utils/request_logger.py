from fastapi import Request
from utils.db_connection import get_db_connection, close_db_connection

async def log_endpoint_stats(request: Request, call_next):
    """
    Middleware to log each API request into the `endpoints` table.
    """
    method = request.method
    path = request.url.path

    # Skip logging for certain paths (e.g., static files, favicon, etc.)
    if path.startswith("/static") or path == "/favicon.ico" or request.method == "OPTIONS":
        return await call_next(request)

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

    # Process the request and return the response
    response = await call_next(request)
    return response
