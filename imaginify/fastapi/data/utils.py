import json
import bcrypt
from util.errors import NotFoundError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw.decode('utf-8')

def read_data():
    try :
        with open('data/users.json', 'r') as f:
            data = json.load(f)
    except :
        logging.error('Data file users.json not found')
        exit()
    return data

def write_data(users):
    try :
        with open('data/users.json', 'w') as f:
            json.dump(users, f, indent=4)
    except :
        logging.error('data file users.json not found')
        exit()

def read_posts():
    try : 
        with open('data/posts.json', 'r') as f:
            data = json.load(f)
    except :
        logging.error('data file posts.json not found')
        exit()
    return data


def write_posts(post):
    try : 
        with open('data/posts.json', 'w') as f:
            json.dump(post, f, indent=4)
    except :
        logging.error('data file posts.json not found')
        exit()

