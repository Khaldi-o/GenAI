from fastapi import APIRouter
from pydantic import BaseModel


from util.validation import is_valid_email, is_valid_text
from util.auth import is_valid_password, create_json_token, is_valid_password
from data.user import get, add
from util.errors import NotAuthError



class Authentificate(BaseModel):
    email : str
    password : str


router_auth = APIRouter()


@router_auth.post("/signup")
def signup(auth : Authentificate):
    email = auth.email
    password = auth.password

    errors = {}

    if not is_valid_email(email):
        errors['email'] = "Invalid email. Must be with a @"
    else :
        try : 
            get(email)
            errors['email'] = "An account with this email already exists. Please log in or use a different email."
        except :
            pass
    
    if not is_valid_text(password, 6):
        errors['password'] = "Invalid password. Must be at least 6 characters long."

    if errors != {} :
        raise NotAuthError(errors)
    
    try :
        user = add({"email": email, "password": password})
        auth_token = create_json_token(email)
        return {
            "message": "User created.",
            "user": user,
            "token": auth_token
        }
    except :
        raise NotAuthError({"message": "Failed to create user."})




@router_auth.post('/login')
def login(auth : Authentificate):
    email = auth.email
    password = auth.password

    user = get(email)
    if user is None :
        raise NotAuthError({"message" : "Invalid credentials."})
    
    if not is_valid_text(password, 6):
        raise NotAuthError({"message" : "Invalid credentials."})
    
    pwIsValid = is_valid_password(password, user['password'])
    if not pwIsValid :
        raise NotAuthError({"message" : "Invalid credentials."})

    auth_token = create_json_token(email)

    return {
            "message": "User signed.",
            "user": user,
            "token": auth_token
    }

