from fastapi import APIRouter, Header
from routes.gen import Details, SocialMedia, ImageSchema, Language, STYLE_IN_FRENCH
from routes.post import Publication
import jwt
from data.post import add, get_post_by_id, post_status_to_posted
from data.user import get, decrement_text_credit, decrement_image_credit
from util.auth import KEY
from util.errors import GeneratingError, NotAuthError, PostingError



router_test = APIRouter()


# Route de test
@router_test.post("/test")
async def create_content(details: Details, authorization = Header(None)):

    jwt_token = authorization.split("Bearer ")[1]
    if not jwt_token:
        raise NotAuthError({"message" : "No token provided"})
    decoded_payload = jwt.decode(jwt_token, KEY, algorithms=['HS256'])
    email = decoded_payload.get('email')
    user = get(email)
    id_user = user['id']

    if user["text_credit"] == 0 or user["image_credit"] == 0:
        raise GeneratingError({"message":"No credit left"})
    

    language = details.language
    network = details.network.value
    subject = details.subject
    style = details.style
    content = details.content
    nb_characters = details.nb_characters
    OutputLanguage = details.OutputLanguage
    if language == Language.FRENCH.value:
        style = STYLE_IN_FRENCH[style]
    text = f"Publication on {network} about {subject} in a {style} style.\nThe post deals with : \n{content}\nWords : {nb_characters}\nLanguage : {language}\nPost language :{OutputLanguage}"

    image_url_1 = "https://c.pxhere.com/images/43/39/d40838b809e4f705c01b9db17b3c-1422617.jpg!d"
    image_url_2 = "https://img.freepik.com/photos-premium/image-galaxie-coloree-dans-ciel-ai-generative_791316-9864.jpg?w=2000"
    image_url_3 = image_url_1
    image_url_4 = image_url_2

    images=[{'id': 'a', 'url' : image_url_1},
            {'id': 'b', 'url' : image_url_2},
            {'id': 'c', 'url' : image_url_3},
            {'id': 'd', 'url' : image_url_4},]
    
    decrement_text_credit(id_user)
    decrement_image_credit(id_user)
    
    return {"network": network, "text" : text, 
            "images" : images, "text_credit" : user["text_credit"]-1, 
            "image_credit" : user["image_credit"]-1,
            "subject": subject}



@router_test.post("/test/text")
async def create_content(details: Details, authorization = Header(None)):

    jwt_token = authorization.split("Bearer ")[1]
    if not jwt_token:
        raise NotAuthError({"message" : "No token provided"})
    decoded_payload = jwt.decode(jwt_token, KEY, algorithms=['HS256'])
    email = decoded_payload.get('email')
    user = get(email)
    id_user = user['id']

    if user['text_credit'] == 0:
        raise GeneratingError({"message":"No credit left"})
    

    language = details.language
    network = details.network.value
    subject = details.subject
    style = details.style
    content = details.content
    nb_characters = details.nb_characters
    OutputLanguage = details.OutputLanguage
    text = f"Publication on {network} about {subject} in a {style} style.\nThe post deals with : \n{content}\nWords : {nb_characters}\nLanguage : {language}\nPost language :{OutputLanguage}"
    
    decrement_text_credit(id_user)
    
    return {"network": network, "text" : text, 
            "prompt_image" : "PROMPT_IMAGE_SENT_BY_TEST_ROUTE", 
            "text_credit" : user["text_credit"]-1,
            "subject": subject}



@router_test.post("/test/image")
async def create_content_image(image_schema: ImageSchema, authorization = Header(None)):

    jwt_token = authorization.split("Bearer ")[1]
    if not jwt_token:
        raise NotAuthError({"message" : "No token provided"})
    decoded_payload = jwt.decode(jwt_token, KEY, algorithms=['HS256'])
    email = decoded_payload.get('email')
    user = get(email)
    id_user = user['id']

    if user['image_credit'] == 0:
        raise GeneratingError({"message":"No credit left"})
    network = image_schema.network
    image_prompt = image_schema.image_prompt

    image_url_1 = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.akamai.com%2Ffr%2Fproducts%2Fimage-and-video-manager&psig=AOvVaw1EioFEYST84AppBL7J63Tz&ust=1700907441408000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCMC3nJC03IIDFQAAAAAdAAAAABAR"
    image_url_2 = "https://img.freepik.com/photos-premium/image-galaxie-coloree-dans-ciel-ai-generative_791316-9864.jpg?w=2000"
    image_url_3 = image_url_1
    image_url_4 = image_url_2

    images=[{'id': 'a', 'url' : image_url_1},
            {'id': 'b', 'url' : image_url_2},
            {'id': 'c', 'url' : image_url_3},
            {'id': 'd', 'url' : image_url_4},]
    
    decrement_image_credit(id_user)

    return {"network" : network, "images" : images, "image_credit" : user["image_credit"]-1}

    

# Route de publication
@router_test.post("/publish_test/{network}")
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

    if network == SocialMedia.LINKEDIN:
        return {"message" : "Post created"}
    elif network == SocialMedia.TWITTER:
        # Post to Twitter
        pass
    elif network == SocialMedia.FACEBOOK:
        # Post to Facebook
        pass
    elif network == SocialMedia.BLOG:
        # Post to Blog
        pass
    elif network == SocialMedia.INSTAGRAM:
        # Post to Instagram
        pass
    else:
        print('Unknown platform')
    
