import bcrypt
import jwt
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from util.errors import NotAuthError


KEY = 'supersecret'

def create_json_token(email):
    return jwt.encode({'email': email}, KEY, algorithm='HS256')


def validate_json_token(token):
    try:
        return jwt.decode(token, KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        # Gérer ici le cas où le token a expiré
        raise Exception('Token expired')
    except jwt.InvalidTokenError:
        # Gérer ici le cas où le token est invalide
        raise Exception('Invalid token')
    
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw.decode('utf-8')

def is_valid_password(password, stored_password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))


class jwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise NotAuthError("Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise NotAuthError("Invalid token or expired token.")
            return credentials.credentials
        else:
            raise NotAuthError("Invalid authorization code.")
        
    def verify_jwt(self, jwtoken: str):
        isTokenValid: bool = False
        if jwt.decode(jwtoken, KEY, algorithms=['HS256']):
            isTokenValid = True
        return isTokenValid
