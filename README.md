# isa_final_project
Final project for ISA

# to start venv, do python -m venv venv first
venv\Scripts\activate to activate venv when in backend, deactivate when done

activating will let you install dependencies only in venv file and not globally on computer

# for when you are cd in backend
pip freeze > requirements.txt when you're done install any new dependencies

pip install -r requirements.txt (do while in venv, installs all dependencies in requirements.txt)

# to start api server
uvicorn main:app --reload 

# to start frontend (in the frontend directory)
npm install
npm run frontend

# required libraries:
transformers - for huggingface access

torch - transformers needs it

fastapi - web framework for building apis

uvicorn - ASGI server

python-dotenv - for env vars

mysql-connector-python - for connection to mysql db

# more libraries probably coming for jwt/authentication (someone decide) and for hashing (probably bcrypt)
