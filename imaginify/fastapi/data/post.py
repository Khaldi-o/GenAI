from data.utils import read_posts, write_posts
from datetime import datetime
import pytz
import uuid
from util.errors import NotFoundError
import os
import requests
import logging

def save_image(url, id_user, id_post):

    if not os.path.exists(f"data/images/{id_user}"):
        os.makedirs(f"data/images/{id_user}")
    response = requests.get(url, verify=False)
    print(response)
    if response.status_code == 200:
        imagePath = os.path.join(f"data/images/{id_user}", id_post)
        with open(imagePath, 'wb') as file:
            file.write(response.content)
    return imagePath



# Function to add a post
def add(data):
    posts = read_posts()

    id = str(uuid.uuid4())
    actual_date = datetime.now(pytz.timezone('Europe/Paris'))
    actual_date = actual_date.isoformat()
    

    image_url = data['image']
    try : 
        image_path = save_image(image_url, data["owner"], id)
    except : 
        logging.error('Image file not created')
        exit()


    new_post = {
        "id": id,
        "owner": data['owner'],
        "network": data['network'], 
        "text": data['text'],
        "subject": data['subject'],
        "imagePath": image_path,
        "date": actual_date,
        "is_posted" : 0
    }


    posts.append(new_post)
    write_posts(posts)
    return new_post




def get_post_by_id(id_post):
    posts = read_posts()

    for post in posts:
        if post['id'] == id_post:
            return post

    raise NotFoundError({"message": "No post with this id exists"})


def get_posts_by_user(id_user):
    posts = read_posts()
    user_posts = []

    for post in posts:
        if post["owner"] == id_user : 
            user_posts.append(post)
    return user_posts



def post_status_to_posted(id):
    posts = read_posts()

    for post in posts:
        if post['id'] == id:
            post['is_posted'] = 1
            write_posts(posts)
            return 'ok'
        
    raise NotFoundError({"message": f"Could not find user for id {id}"})







