from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import jwt
from jwt import encode as jwt_encode
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from bson import ObjectId
import uvicorn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
 username: str = None # Make the username field optional
 email: str
 password: str

 # MongoDB connection
# client = MongoClient("mongodb://localhost:27017")
# db = client["mydatabase"]
# users_collection = db["users"]
DATABASE_ACCESS = "mongodb+srv://Serbian:Serbian@cluster0.trfcrdw.mongodb.net/mytable?retryWrites=true&w=majority"
ACCESS = "mongodb+srv://Serbian:Serbian@cluster0.trfcrdw.mongodb.net/"

# Konekcija na MongoDB Atlas bazu podataka
client = MongoClient(DATABASE_ACCESS)

# Odabir baze
db = client.get_database()

users_collection = db.mytable

SECRET_KEY = "your-secret-key-goes-here"
security = HTTPBearer()

@app.get("/")
def homepage():
 return {"message": "Welcome to the homepage"}

@app.post("/login")
def login(user: User):
    # Check if user exists in the database
    user_data = users_collection.find_one(
    {"email": user.email, "password": user.password}
    )
    if user_data:
        # Generate a token
        # Convert ObjectId to string
        token = generate_token(user.email)
        user_data["_id"] = str(user_data["_id"])
        return user_data
    
    return {"message": "Invalid email or password"}

@app.post("/register")
def register(user: User):
 # Check if user already exists in the database
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        return {"message": "User already exists"}
    # Insert the new user into the database
    user_dict = user.model_dump()
    users_collection.insert_one(user_dict)
    token = generate_token(user.email)
    # Convert ObjectId to string
    user_dict["_id"] = str(user_dict["_id"])
    user_dict["token"] = token
    return user_dict

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/api/user")
def get_user(credentials: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(credentials, SECRET_KEY, algorithms=["HS256"])
        user_data = {
            "username": payload.get("email"),  # Pretpostavka da je email u JWT payloadu
            "email": payload.get("email")
        }
        return user_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def generate_token(email: str) -> str:
 payload = {"email": email}
 token = jwt_encode(payload, SECRET_KEY, algorithm="HS256")
 return token

if __name__ == "__main__":
 import uvicorn
 uvicorn.run(app, host="0.0.0.0", port=8001)