# comp4968final_project
Final project for COMP4968: Serverless computing and microservices

# to start venv, do python -m venv venv first
# venv\Scripts\activate to activate venv when in backend, deactivate when done
# activating will let you install dependencies only in venv file and not globally on computer

# pip freeze > requirements.txt when exporting to digitalocean for dependencies
# pip install -r requirements.txt afterwards (do while in venv)

# required libraries:
# transformers - for huggingface access
# torch - transformers needs it
# fastapi - web framework for building apis
# uvicorn - ASGI server
# python-dotenv - for env vars