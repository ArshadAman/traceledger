from pydantic import BaseModel, EmailStr, Field

class CreateUserRequest(BaseModel):
    email: EmailStr
    role: str
    password: str = Field(min_length=8)
   
class UserResponse(BaseModel):
    id: int
    email: EmailStr