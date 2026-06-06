from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class User (BaseModel):
    name : str
    age : int

users = []

#create user
@app.post ("/users")
def create_users(user: User):
    users.append(user)
    return {
        "message": "user created successfully",
        "data" : user
    }
#get all users
@app.get("/users")
def get_users():
    return users 

#get user by id
@app.get("/users/{user_id}")
def get_user_id (user_id: int):
    if user_id < 0 or user_id >= len (users):
        return {"error": "user not found"}
    return users [user_id]

#update user
@app.put ("/users/{user_id}")
def update_user (user_id:int, user:User):
    if user_id < 0 or user_id >= len(users):
        return {"error": "user not found"}
    
    users[user_id] = user
    return {
        "message": "User updated",
        "data":  user
    }

#remove User
@app.delete ("/users/{user_id}")
def delete_user (user_id: int):
    if user_id < 0 or user_id >= len(users):
        return {"error": "user not found"}
    
    removed_user = users.pop(user_id)
    return {"message": "user deleted",
            "data":removed_user}