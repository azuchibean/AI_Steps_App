
# AI Steps App

This repository contains the final project for ISA, which involves building an API server using FastAPI. The project is designed with modularity and efficiency in mind, leveraging popular libraries and frameworks.

---

## Project Setup

### 1. Virtual Environment Setup
It is recommended to use a virtual environment to manage dependencies.

- To create a virtual environment:
  ```bash
  python -m venv venv
  ```
- To activate the virtual environment (when in the `backend` directory):
  ```bash
  venv\Scripts\activate
  ```
- To deactivate the virtual environment:
  ```bash
  deactivate
  ```

### 2. Dependency Management
- To install dependencies from `requirements.txt` (ensure the virtual environment is activated):
  ```bash
  pip install -r requirements.txt
  ```

---

## Running the API Server

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Start the server using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

The server will run on `http://127.0.0.1:8000` by default. Use `--host` and `--port` options to customize if needed.

---

## Required Libraries

Below are the key libraries used in this project along with their purposes:

| Library                  | Purpose                                                |
|--------------------------|--------------------------------------------------------|
| `transformers`           | Access to HuggingFace's pre-trained models and tools.  |
| `torch`                  | Required for `transformers` to function.               |
| `fastapi`                | Web framework for building APIs.                       |
| `uvicorn`                | ASGI server for running the FastAPI application.       |
| `python-dotenv`          | For managing environment variables.                    |
| `mysql-connector-python` | MySQL database connection.                             |
| `requests`               | To make HTTP requests (e.g., email APIs).              |
| `passlib`                | Manages multiple password hashing algorithms.          |
| `bcrypt`                 | For secure password hashing.                           |
| `python-jose`            | JSON Web Token (JWT) support for authentication.       |
| `cryptography`           | Provides cryptographic recipes and primitives.                                              |
| `geopy`                  | Geocoding and geographical calculations.                                                    |
| `pydantic`               | Data validation and parsing using Python type hints.                                        |
---

## API Documentation

FastAPI includes Swagger support out of the box, making it easy to view and test API endpoints.

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
2. Open your browser and go to:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

This will display the auto-generated Swagger UI, where you can interact with the API.

---

## Additional Notes

- **Environment Variables**: Use `.env` files to store sensitive information such as database credentials or API keys. Make sure to include `.env` in your `.gitignore` file.
- **Password Management**: `passlib` and `bcrypt` are available for hashing and verifying passwords. These libraries may be included as needed.
- **JWT Authentication**: `python-jose` is used to handle token-based authentication, providing secure and scalable user authentication.
