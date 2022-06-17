from pydantic import BaseModel, constr, validator
from typing import Optional, Union
import string

def validate_username(username: str)-> str:
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "Invalid characters in username."
    assert len(username) >= 3, "Username must be 3 characters or more."
    return username

class UserBase(BaseModel):
    username : Optional[str]
    
class User(UserBase):
    id : Optional[int]
    role : Optional[bool] = False # True -> super user | False -> normal user 
    hashed_password : Optional[str]

class UserCreate(UserBase):
    password : constr(min_length=3, max_length=100)
    @validator("username", pre=True)
    def username_is_valid(cls, username: str)-> str:
        return validate_username(username=username)

class UserInDB(User):
    pass

class UserPublic(UserBase):
    pass

if __name__ == "__main__":
    a = UserCreate(username="teca", password="123")
    b = User(username=a.username, id =1, hashed_password=a.password)
    print(b)    
    z = UserPublic(username=b.username)
    
    