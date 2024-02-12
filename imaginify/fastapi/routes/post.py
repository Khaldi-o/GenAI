from fastapi import APIRouter, Header
from util.posting import post_to_linkedin
from pydantic import BaseModel
from enum import Enum
import jwt
from data.post import add, get_post_by_id, get_posts_by_user, post_status_to_posted
from data.user import get
from util.auth import KEY
from util.errors import PostingError


class SocialMedia(Enum):
    LINKEDIN = 'linkedin'
    TWITTER = 'twitter'
    FACEBOOK = 'facebook'
    BLOG = 'blog'
    INSTAGRAM = 'instagram'

class Publication(BaseModel):
    text: str
    image : str
    subject : str
    network : SocialMedia

router_post = APIRouter()


@router_post.post("/save")
def save(publication : Publication, authorization = Header(None)):

    jwt_token = authorization.split("Bearer ")[1]
    decoded_payload = jwt.decode(jwt_token, KEY, algorithms=['HS256'])
    email = decoded_payload.get('email')
    user = get(email)
    id_user = user['id']

    # add publication in database
    post = add({"owner": id_user, 
                "network" : publication.network.value, 
                "text": publication.text, 
                "image": publication.image,
                "subject": publication.subject})
    return {"id": post["id"]}


@router_post.get("/post/{post_id}")
def get_post(post_id : str):
    return get_post_by_id(post_id)

@router_post.get("/posts/{user_id}")
def get_posts(user_id : str):
    return get_posts_by_user(user_id)


# Route de publication
@router_post.post("/publish")
def post_publication(id_publication, authorization = Header(None)):

    jwt_token = authorization.split("Bearer ")[1]
    decoded_payload = jwt.decode(jwt_token, KEY, algorithms=['HS256'])
    email = decoded_payload.get('email')
    user = get(email)
    id_user = user['id']

    post = get_post_by_id(id_publication)

    if post["owner"] != id_user : 
        raise PostingError({'message': 'permission denied'})

    text = post["text"]
    imagePath = post["imagePath"]
    network = post["network"]
    post_status_to_posted(post["id"])

    if network == SocialMedia.LINKEDIN.value:
        try :
            post_to_linkedin(text, imagePath)
            return {"message" : "Post created"}
        except PostingError as e: 
            raise PostingError({"message": e.detail})
    elif network == SocialMedia.TWITTER.value:
        # Post to Twitter
        pass
    elif network == SocialMedia.FACEBOOK.value:
        # Post to Facebook
        pass
    elif network == SocialMedia.BLOG.value:
        # Post to Blog
        pass
    elif network == SocialMedia.INSTAGRAM.value:
        # Post to Instagram
        pass
    else:
        print('Unknown network')
