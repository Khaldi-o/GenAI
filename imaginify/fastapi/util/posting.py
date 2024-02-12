import os
import requests
import json
from data.post import add
from util.errors import PostingError

access_token = os.getenv('LINKEDIN_AUTH_TOKEN')

def get_urn():
    # On récupère l'URN de l'utilisateur
    try : 
        api_url_base = 'https://api.linkedin.com/v2/'
        headers = {
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {access_token}"
        }
        response = requests.get(api_url_base + 'userinfo', headers=headers, verify=False)
        URN = response.json()['sub']
        return URN
    except : 
        raise PostingError("LinkedIn user not found")



def register_image(URN):
    try : 
        url = 'https://api.linkedin.com/v2/assets?action=registerUpload'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        payload = {
            "registerUploadRequest": {
                "recipes": [
                    "urn:li:digitalmediaRecipe:feedshare-image"
                ],
                "owner": f"urn:li:person:{URN}",
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        upload_url = response.json()["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        asset = response.json()["value"]["asset"]
        print("UPLOAD URL : ", upload_url)
        print("ASSET : ", asset)
        return upload_url, asset
    except : 
        raise PostingError("An error occurred while registering the image")

def upload_image(image, upload_url):
    try : 

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        files = {
            'file': open(image, 'rb')
        }

        response = requests.post(upload_url, headers=headers, files=files)

    except : 
        raise PostingError("An error occurred while uploading the image")
    
def create_share(URN, texte, asset):
    try :

        api_url_base = 'https://api.linkedin.com/v2/'

        post_data = {
            "author": f"urn:li:person:{URN}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": texte
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {
                                "text": "TEST "
                            },
                            "media": asset,
                            "title": {
                                "text": "image"
                            }
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        headers = {
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {access_token}"
        }

        response = requests.post(api_url_base + 'ugcPosts', headers=headers, json=post_data, verify=False)

        if response.status_code == 201:
            print("Success")
            print(response.content)
        else:
            print(response.content)
    except : 
        raise PostingError("An error occurred while sharing the post")

        

def post_to_linkedin(text, image):
    
    try :
        urn = get_urn()
        upload_url, asset = register_image(urn)
        upload_image(image, upload_url)
        create_share(urn, text, asset)
    except Exception as e : 
        raise PostingError(f"An error occurred : {str(e)}")

