from pydantic import BaseModel

class User(BaseModel):
    username: str
    id_rol: int

class UserInDB(User):
    mail: str
    password: str