from pydantic import BaseModel
from typing import List

class RegisterRequest(BaseModel):
    first_name: str
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Victor",
                "email": "victorfung@example.com",
                "password": "$2b$12$eIX6Oa1hXoJb7S5C7EqOiEM4Txp06hz9P8zoN7dTFSdIjHp51sbQm"
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

class PasswordResetRequest(BaseModel):
    email: str

class PasswordReset(BaseModel):
    token: str
    new_password: str

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
