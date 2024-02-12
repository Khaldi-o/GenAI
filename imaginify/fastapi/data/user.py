import uuid
import json

from util.auth import hash_password
from util.errors import NotAuthError
from data.utils import read_data, write_data
import schedule
import time
import threading
import datetime
import pytz


INITIAL_CREDIT = 200


# Function to add an user
def add(data):
    users = read_data()

    user_id = str(uuid.uuid4())
    hashed_pw = hash_password(data['password'])

    new_user = {
        "id": user_id,
        "email": data['email'],
        "password": hashed_pw,
        "text_credit" : INITIAL_CREDIT,
        "image_credit" : INITIAL_CREDIT
    }

    users.append(new_user)
    write_data(users)
    return {"id": user_id, "email": data['email'], "text_credit" : INITIAL_CREDIT, "image_credit" : INITIAL_CREDIT}


# Function to get an user
def get(email):
    users = read_data()

    for user in users:
        if user['email'] == email:
            return user

    raise NotAuthError({"message": f"Could not find user for email {email}"})


def decrement_text_credit(id):
    users = read_data()

    for user in users:
        if user['id'] == id:
            user['text_credit'] -= 1
            write_data(users)
            return 'ok'
        
    raise NotAuthError({"message": f"Could not find user for id {id}"})

def decrement_image_credit(id):
    users = read_data()

    for user in users:
        if user['id'] == id:
            user['image_credit'] -= 1
            write_data(users)
            return 'ok'
        
    raise NotAuthError({"message": f"Could not find user for id {id}"})




def reset_credit():
    users = read_data()

    for user in users:
        user['text_credit'] = INITIAL_CREDIT
        user['image_credit'] = INITIAL_CREDIT
    write_data(users)



# Fonctions pour planifier la réinitialisation au début de chaque mois
def check_and_reset():
    now = datetime.datetime.now(pytz.timezone('Europe/Paris'))
    if now.day == 1:  # Si c'est le premier jour du mois
        reset_credit()

def schedule_reset():
    schedule.every().day.at('00:00:01').do(check_and_reset)


# Fonction pour démarrer la planification
def start_scheduler():
    schedule_reset()
    while True:
        schedule.run_pending()
        time.sleep(1)


scheduler_thread = threading.Thread(target=start_scheduler)
scheduler_thread.start()



