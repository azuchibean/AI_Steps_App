from pydantic import BaseModel
from typing import List, Optional

class RegisterRequest(BaseModel):
    first_name: str
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "email": "user@example.com",
                "password": "12345678"
            }
        }
        
class RegisterResponse(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "User registered successfully!"
            }
        }

class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "Login successful",
                "password": "12345678"
            }
        }


class LoginResponse(BaseModel):
    message: str
    isAdmin: int

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Login successful",
                "isAdmin": 0
            }
        }

class LogoutResponse(BaseModel):
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Logged out successfully"
            }
        }

class PasswordResetRequest(BaseModel):
    email: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }

class PasswordResetRequestResponse(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Password reset link has been sent to your email"
            }
        }

class PasswordReset(BaseModel):
    token: str
    new_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "token": "example-reset-token",
                "new_password":"password"
            }
        }

class PasswordResetResponse(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Password has been reset successfully"
            }
        }

class VerifyTokenResponse(BaseModel):
    message: str
    user_id: int
    user: str
    isAdmin: int
    free_api_calls_remaining: int
    total_api_calls: int
    first_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Token is valid",
                "user_id": 123,
                "user": "user@example.com",
                "isAdmin": 1,
                "free_api_calls_remaining": 19,
                "total_api_calls": 1,
                "first_name": "John"
            }
        }


class LocationDetails(BaseModel):
    latitude: float
    longitude: float
    height: int
    steps: int
    location_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 49.224090,
                "longitude": -123.063501,
                "height": 180,
                "steps": 1000,
                "location_type": "park"
            }
        }

class ApiResponseItem(BaseModel):
    name: str
    address: str
    distance: float
    rating: float
    url: str

class ApiResponse(BaseModel):
    api_response: List[ApiResponseItem]
    llm_recommendation: str

class LocationDetailsResponse(BaseModel):
    response: ApiResponse

    class Config:
        json_schema_extra = {
            "example": {
                "response": {
                    "api_response": [
                        {
                            "name": "Bobolink Park",
                            "address": "2510 Hoylake Avenue, Vancouver",
                            "distance": 1108.2,
                            "rating": 4.4,
                            "url": "https://www.google.com/maps/place/?q=place_id:ChIJTU9RhTJ0hlQReT_ozcd7LFU"
                        },
                        {
                            "name": "Gordon Park",
                            "address": "6675 Commercial Street, Vancouver",
                            "distance": 422.15,
                            "rating": 4.3,
                            "url": "https://www.google.com/maps/place/?q=place_id:ChIJ____Ezt0hlQRbH4nQIeSKys"
                        },
                        {
                            "name": "Humm Park",
                            "address": "7250 Humm Street, Vancouver",
                            "distance": 592.44,
                            "rating": 4.2,
                            "url": "https://www.google.com/maps/place/?q=place_id:ChIJq6rqyDF0hlQRXLjveZ83HR8"
                        }
                    ],
                    "llm_recommendation": "Bobolink Park"
                }
            }
        }

class EndpointStatsResponse(BaseModel):
    method: str
    endpoint: str
    count: int

class EndpointStatsListResponse(BaseModel):
    endpoints: List[EndpointStatsResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "endpoints": [
                    {
                    "method": "POST",
                    "endpoint": "/api/v1/register",
                    "count": 9
                    },
                    {
                    "method": "POST",
                    "endpoint": "/api/v1/login",
                    "count": 54
                    },
                    {
                    "method": "GET",
                    "endpoint": "/api/v1/stats/apiUsage",
                    "count": 80
                    },
                ]
            }
        }


class ApiUsageResponse(BaseModel):
    first_name: str
    email: str
    total_api_calls: int
    
class ApiUsageListResponse(BaseModel):
    users: List[ApiUsageResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "users": [
                    {"first_name": "bob", "email": "bob@gmail.com", "total_api_calls": 53},
                    {"first_name": "angela", "email": "angela@gmail.com", "total_api_calls": 11}
                ]
            }
        }

class ApiUsageForUserResponse(BaseModel):
    id: int
    user_id: int
    total_api_calls: int
    llm_api_calls: int
    warning: Optional[str] = None
    free_calls_remaining: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "total_api_calls": 233,
                "llm_api_calls": 0,
                "warning": None,
                "free_calls_remaining": 20
            }
        }
    
class UpdateNameResponse(BaseModel):
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Name updated successfully"
            }
        }

class DeleteAccountResponse(BaseModel):
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Account deleted successfully"
            }
        }
