
# ISA Final Project

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
- After installing any new dependencies, update the `requirements.txt` file:
  ```bash
  pip freeze > requirements.txt
  ```
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
| `accelerate`             | Optimizes performance for distributed processing.      |
| `annotated-types`        | Provides type annotations for enhanced type checking and validation.                        |
| `anyio`                  | A compatibility layer for asynchronous Python libraries.                                    |
| `certifi`                | Provides secure SSL/TLS certificates.                                                       |
| `cffi`                   | A Foreign Function Interface for calling C code from Python.                                |
| `charset-normalizer`     | Detects and normalizes character encodings in text data.                                    |
| `click`                  | A library for creating command-line interfaces.                                             |
| `colorama`               | Enables cross-platform colored terminal text.                                               |
| `cryptography`           | Provides cryptographic recipes and primitives.                                              |
| `ecdsa`                  | Implements elliptic curve cryptography.                                                     |
| `filelock`               | A cross-platform file locking mechanism.                                                    |
| `fsspec`                 | File system specification for reading/writing data.                                         |
| `geographiclib`          | Geodetic calculations and utilities.                                                        |
| `geopy`                  | Geocoding and geographical calculations.                                                    |
| `h11`                    | An HTTP/1.1 protocol implementation.                                                        |
| `huggingface-hub`        | Tools for interacting with Hugging Face's model repository.                                 |
| `idna`                   | Handles internationalized domain names.                                                     |
| `Jinja2`                 | A template engine for Python.                                                               |
| `MarkupSafe`             | Provides safeguards against code injection in templates.                                     |
| `mpmath`                 | Library for arbitrary-precision arithmetic.                                                 |
| `networkx`               | Tools for creating and analyzing complex networks/graphs.                                    |
| `numpy`                  | A library for numerical computing in Python.                                                |
| `packaging`              | Utilities for packaging and dependency management.                                           |
| `psutil`                 | Utilities for accessing system and process information.                                      |
| `pyasn1`                 | ASN.1 data structures support for Python.                                                   |
| `pycparser`              | A parser for C code, used in `cffi`.                                                        |
| `pydantic`               | Data validation and parsing using Python type hints.                                        |
| `pydantic_core`          | Optimized core for `pydantic`.                                                              |
| `PyYAML`                 | Reads and writes YAML files.                                                                |
| `regex`                  | Provides enhanced regular expression capabilities.                                          |
| `rsa`                    | Implements the RSA encryption algorithm.                                                    |
| `safetensors`            | Loads tensor data in a secure format.                                                       |
| `six`                    | Provides compatibility between Python 2 and 3.                                              |
| `sniffio`                | Detects the async library in use.                                                           |
| `starlette`              | ASGI framework used by FastAPI.                                                             |
| `sympy`                  | A library for symbolic mathematics.                                                         |
| `tokenizers`             | Tokenization tools for machine learning models.                                             |
| `tqdm`                   | Displays progress bars in Python loops.                                                     |
| `typing_extensions`      | Backported features for type hints.                                                         |
| `urllib3`                | A robust HTTP library for Python.                                                           |

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
