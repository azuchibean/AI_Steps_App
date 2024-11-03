#temp name for this file

from pydantic import BaseModel

class RegisterRequest(BaseModel):
    first_name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class PasswordResetRequest(BaseModel):
    email: str

class PasswordReset(BaseModel):
    token: str
    new_password: str