from fastapi import APIRouter, Header
from fastapi import HTTPException
from util.generate import askOpenAI, drawDalle3
from routes.post import SocialMedia
from pydantic import BaseModel
import jwt
from data.user import get, decrement_text_credit, decrement_image_credit
from util.auth import KEY
from util.errors import GeneratingError, NotAuthError, LanguageError
from enum import Enum

class Language(Enum):
    ENGLISH = "english"
    FRENCH = "french"

class OutputLanguage(Enum):
    ENGLISH = "english"
    FRENCH = "french"

STYLE_IN_FRENCH = {
    "professional": "professionnel",
    "quirky": "excentrique",
    "educational": "éducatif",
    "funny": "drôle",
    "analytic": "analytique",
    "prospective": "prospectif",
    "inspiring": "inspirant",
    "innovative": "innovant",
    "avant-garde": "avant-gardiste",
    "critic": "critique",
    "engaging": "captivant"
}

class Details(BaseModel):
    network: SocialMedia
    subject: str
    style: str
    content: str
    nb_characters: str
    language: str
    OutputLanguage: str


router_gen = APIRouter()


# Route de génération de contenu
@router_gen.post("/content")
async def create_content(details: Details, authorization=Header(None)):
    jwt_token = authorization.split("Bearer ")[1]
    if not jwt_token:
        raise NotAuthError({"message": "No token provided"})
    decoded_payload = jwt.decode(jwt_token, KEY, algorithms=["HS256"])
    email = decoded_payload.get("email")
    user = get(email)
    id_user = user["id"]

    if user["text_credit"] == 0 or user["image_credit"] == 0:
        raise GeneratingError({"message": "No credit left"})

    language = details.language
    network = details.network.value
    subject = details.subject
    style = details.style
    content = details.content
    nb_characters = details.nb_characters
    OutputLanguage = details.OutputLanguage


    #if OutputLanguage not in [lang.value for lang in OutputLanguage]:
    #    raise HTTPException(status_code=400, detail="Select a valid output language.")

    
    if language not in [lang.value for lang in Language]:
        raise LanguageError({"message": "Select a valid language."})
    if language == Language.FRENCH.value:
        style = STYLE_IN_FRENCH[style]

    if network == SocialMedia.BLOG.value:

        if language == Language.ENGLISH:
            system_prompt = "You are a blogger, expert in writing blog posts.\nFormat your response using HTML. Use headings, subheadings, bullets and bold to organize the information. The text must be easy to read and understand, with title, subtitles and different parts and sub-parts."
            user_prompt = "I want you to act as a blogger and want to write a blog post on "
            user_prompt += subject
            user_prompt += ", with a "
            user_prompt += style
            user_prompt += " and accessible tone that engages readers. I want you to include this information : \n"
            user_prompt += content
            user_prompt += "\n\nThe blog must include all of the information above, and must contain "
            user_prompt += nb_characters
            user_prompt += " characters. Simply write the blog, without adding anything around it. Use if necessary, emojis and hashtags. Write in "
            user_prompt += OutputLanguage
            user_prompt += "."

        if language == Language.FRENCH.value:
            system_prompt = "Vous êtes un blogueur, expert en l'écriture d'article de blog.\nFormatez votre réponse en utilisant le HTLM. Utilisez des titres, des sous-titres, des puces et des caractères gras pour organiser les informations. Le texte doit être facile à lire et à comprendre, avec titre, sous-titres et différentes parties et sous parties."
            user_prompt = "Je veux que vous agissez en tant que blogueur et que vous souhaitiez écrire un article de blog sur "
            user_prompt += subject
            user_prompt += ", avec un ton "
            user_prompt += style
            user_prompt += " et accessible qui engage les lecteurs. Je souhaite que vous incluiez ces informations : \n"
            user_prompt += content
            user_prompt += "\n\nLe blog doit reprendre l'ensemble des informations ci-dessus, et doit faire "
            user_prompt += nb_characters
            user_prompt += " caractères.  Écrivez simplement le blog, sans rien ajouter autour. Utilisez si nécessaire des émojis et des hashtag. Ecrivez en "
            user_prompt += OutputLanguage
            user_prompt += "."
    else:
        if language == Language.ENGLISH.value:
            system_prompt = "You are an expert in communication on "
            system_prompt += network
            system_prompt += ". You write posts on this network perfectly well. You will be asked to write a post in "
            system_prompt += OutputLanguage
            system_prompt += " on a subject, simply write the post without adding anything around it."
            system_prompt += " Do not hesitate to use emojis and #-tags if necessary."

            user_prompt = "You have been hired by a company to create an advertising campaign. You must create a post of "
            user_prompt += nb_characters
            user_prompt += " characters with the subject "
            user_prompt += subject
            user_prompt += " in a "
            user_prompt += style
            user_prompt +=" style.\n\nThe publication must talk about the following content: \n"
            user_prompt += subject
            user_prompt += "\n"
            user_prompt += content
            user_prompt += "\n\nThe publication must respect the formalism of the network and the size of "
            user_prompt += nb_characters
            user_prompt += " characters. Simply write the publication, without anything add around. Use emojis and hashtags if necessary. Write in "
            user_prompt += OutputLanguage
            user_prompt += "."

        if language == Language.FRENCH.value:
            system_prompt = "Vous êtes un expert en communication sur "
            system_prompt += network
            system_prompt += ". Vous écrivez parfaitement bien des posts sur ce réseau. On vous demandera d'écrire un post en "
            system_prompt += language
            system_prompt += " sur un sujet, écrivez simplement le post sans rien ajouter autour."
            system_prompt += " Utilisez si nécessaire des émojis et des hashtags."

            user_prompt = "Vous avez été engagé par une entreprise pour créer une campagne publicitaire. Vous devez créer un post de "
            user_prompt += nb_characters
            user_prompt += " mots avec pour sujet "
            user_prompt += subject
            user_prompt += " dans un style "
            user_prompt += style
            user_prompt += ".\n\nLa publication doit parler du contenu suivant : \n"
            user_prompt += subject
            user_prompt += "\n"
            user_prompt += content
            user_prompt += "\n\nLa publication doit bien respecter le formalisme du réseau et la taille de "
            user_prompt += nb_characters
            user_prompt += " caractères. Écrivez simplement la publication, sans rien ajouter autour."
            user_prompt += "Le contenu généré devrait être dans la langue"
            user_prompt += OutputLanguage
            user_prompt += " Utilisez les émojis et les hashtags si nécessaire."

    post_text = askOpenAI(user_prompt, system_prompt)
    if language == Language.ENGLISH.value:
        prompt_system2 = "You are a prompt engineer, specialized in prompt image generation. Here are some examples :\n1- Woman, beautiful bedroom, glasses, showing skin, soft symmetric facial features, close up portrait, young, shot on sony a1, 85mm F/1. 4 ISO 100, medium format, 45 megapixel, flash lighting, natural sun lighting \n2- photograph close up portrait old tough decorated general, serious, stoic cinematic 4k epic detailed 4k epic detailed photograph shot on kodak detailed bokeh cinematic hbo dark moody \n3- photorealistic young mother walking at the beach, holding hands with her little son, mountains in the background, photography style, 85mm bookeh detailed, high resolution, high quality, natural lighting, ultra-detailed \n4-Landscape photography of snow-covered mountain peaks at sunrise, using natural light. \n5-Portrait photography during the golden hour, using the soft, warm light to highlight the subject."
        prompt_user2 = "Write in english an image prompt in the same format as the examples, capable of generating an image on the content below : \n"
        prompt_user2 += subject
        prompt_user2 += "\n"
        prompt_user2 += content
        prompt_user2 += "\n\nThe size and content of the image must respect the "
        prompt_user2 += network
        prompt_user2 += " formalism. Write only the image prompt, do not add emoji or hashtags."

    if language == Language.FRENCH.value:
        prompt_system2 = "Vous êtes un ingénieur des prompts, spécialisé dans les prompts de génération d'images. Voici quelques examples de prompts:\n1- Woman, beautiful bedroom, glasses, showing skin, soft symmetric facial features, close up portrait, young, shot on sony a1, 85mm F/1. 4 ISO 100, medium format, 45 megapixel, flash lighting, natural sun lighting \n2- photograph close up portrait old tough decorated general, serious, stoic cinematic 4k epic detailed 4k epic detailed photograph shot on kodak detailed bokeh cinematic hbo dark moody \n3- photorealistic young mother walking at the beach, holding hands with her little son, mountains in the background, photography style, 85mm bookeh detailed, high resolution, high quality, natural lighting, ultra-detailed \n4-Landscape photography of snow-covered mountain peaks at sunrise, using natural light. \n5-Portrait photography during the golden hour, using the soft, warm light to highlight the subject."
        prompt_user2 = "Ecrivez en anglais un prompt de génération d'image dans le même format que les exemples, capable de générer une image sur le contenu suivant: \n"
        prompt_user2 += subject
        prompt_user2 += "\n"
        prompt_user2 += content
        prompt_user2 += "\n\nLa taille et le contenu de l'image devront respecter le formalisme du réseau social "
        prompt_user2 += network
        prompt_user2 += ". Ecrivez seulement le prompt pour générer l'image, n'ajoutez pas d'émoji ou de hashtags."

    image_prompt = askOpenAI(prompt_user2, prompt_system2)
    image_url_1 = drawDalle3(image_prompt, network)
    image_url_2 = drawDalle3(image_prompt, network)
    image_url_3 = drawDalle3(image_prompt, network)
    image_url_4 = drawDalle3(image_prompt, network)
    images = [
        {"id": "a", "url": image_url_1},
        {"id": "b", "url": image_url_2},
        {"id": "c", "url": image_url_3},
        {"id": "d", "url": image_url_4},
    ]

    decrement_text_credit(id_user)
    decrement_image_credit(id_user)

    return {
        "network": network,
        "text": post_text,
        "images": images,
        "text_credit": user["text_credit"] - 1,
        "image_credit": user["image_credit"] - 1,
        "subject": subject,
    }


# Route de génération de contenu : juste le texte
@router_gen.post("/content/text")
async def create_content(details: Details, authorization=Header(None)):
    jwt_token = authorization.split("Bearer ")[1]
    if not jwt_token:
        raise NotAuthError({"message": "No token provided"})
    decoded_payload = jwt.decode(jwt_token, KEY, algorithms=["HS256"])
    email = decoded_payload.get("email")
    user = get(email)
    id_user = user["id"]

    if user["text_credit"] == 0:
        raise GeneratingError({"message": "No credit left"})

    language = details.language
    network = details.network.value
    subject = details.subject
    style = details.style
    content = details.content
    nb_characters = details.nb_characters
    OutputLanguage = details.OutputLanguage

    if language not in [lang.value for lang in Language]:
        raise LanguageError({"message": "Select a valid language."})
    if language == Language.FRENCH.value:
        style = STYLE_IN_FRENCH[style]
    if network == SocialMedia.BLOG.value:
        if language == Language.ENGLISH.value:
            system_prompt = "You are a blogger, expert in writing blog posts.\nFormat your response using HTML. Use headings, subheadings, bullets and bold to organize the information. The text must be easy to read and understand, with title, subtitles and different parts and sub-parts."
            user_prompt = "I want you to act as a blogger and want to write a blog post on "
            user_prompt += subject
            user_prompt += ", with a "
            user_prompt += style
            user_prompt += " and accessible tone that engages readers. I want you to include this information : \n"
            user_prompt += content
            user_prompt += "\n\nThe blog must include all of the information above, and must contain "
            user_prompt += nb_characters
            user_prompt += " characters. Simply write the blog, without adding anything around it. Use if necessary, emojis and hashtags. Write in "
            user_prompt += OutputLanguage
            user_prompt += "."

        if language == Language.FRENCH.value:
            system_prompt = "Vous êtes un blogueur, expert en l'écriture d'article de blog.\nFormatez votre réponse en utilisant le HTLM. Utilisez des titres, des sous-titres, des puces et des caractères gras pour organiser les informations. Le texte doit être facile à lire et à comprendre, avec titre, sous-titres et différentes parties et sous parties."
            user_prompt = "Je veux que vous agissez en tant que blogueur et que vous souhaitiez écrire un article de blog sur "
            user_prompt += subject
            user_prompt += ", avec un ton "
            user_prompt += style
            user_prompt += " et accessible qui engage les lecteurs. Je souhaite que vous incluiez ces informations : \n"
            user_prompt += content
            user_prompt += "\n\nLe blog doit reprendre l'ensemble des informations ci-dessus, et doit faire "
            user_prompt += nb_characters
            user_prompt += " caractères.  Écrivez simplement le blog, sans rien ajouter autour. Utilisez si nécessaire des émojis et des hashtag. Ecrivez en "
            user_prompt += OutputLanguage
            user_prompt += "."
    else:
        if language == Language.ENGLISH.value:
            system_prompt = "You are an expert in communication on "
            system_prompt += network
            system_prompt += ". You write posts on this network perfectly well. You will be asked to write a post in "
            system_prompt += OutputLanguage
            system_prompt += " on a subject, simply write the post without adding anything around it."
            system_prompt += " Do not hesitate to use emojis and #-tags if necessary."

            user_prompt = "You have been hired by a company to create an advertising campaign. You must create a post of "
            user_prompt += nb_characters
            user_prompt += " characters with the subject "
            user_prompt += subject
            user_prompt += " in a "
            user_prompt += style
            user_prompt += " style.\n\nThe publication must talk about the following content: \n"
            user_prompt += subject
            user_prompt += "\n"
            user_prompt += content
            user_prompt += "\n\nThe publication must respect the formalism of the network and the size of "
            user_prompt += nb_characters
            user_prompt += " characters. Simply write the publication, without anything add around. Use emojis and hashtags if necessary. Write in "
            user_prompt += language
            user_prompt += "."

        if language == Language.FRENCH.value:
            system_prompt = "Vous êtes un expert en communication sur "
            system_prompt += network
            system_prompt += ". Vous écrivez parfaitement bien des posts sur ce réseau. On vous demandera d'écrire un post en "
            system_prompt += language
            system_prompt += " sur un sujet, écrivez simplement le post sans rien ajouter autour."
            system_prompt += " Utilisez si nécessaire des émojis et des hashtags."

            user_prompt = "Vous avez été engagé par une entreprise pour créer une campagne publicitaire. Vous devez créer un post de "
            user_prompt += nb_characters
            user_prompt += " mots avec pour sujet "
            user_prompt += subject
            user_prompt += " dans un style "
            user_prompt += style
            user_prompt += ".\n\nLa publication doit parler du contenu suivant : \n"
            user_prompt += subject
            user_prompt += "\n"
            user_prompt += content
            user_prompt += "\n\nLa publication doit bien respecter le formalisme du réseau et la taille de "
            user_prompt += nb_characters
            user_prompt += " caractères. Écrivez simplement la publication, sans rien ajouter autour."
            user_prompt += " Utilisez les émojis et les hashtags si nécessaire."

    post_text = askOpenAI(user_prompt, system_prompt)

    if language == Language.ENGLISH.value:
        prompt_system2 = "You are a prompt engineer, specialized in prompt image generation. Here are some examples :\n1- Woman, beautiful bedroom, glasses, showing skin, soft symmetric facial features, close up portrait, young, shot on sony a1, 85mm F/1. 4 ISO 100, medium format, 45 megapixel, flash lighting, natural sun lighting \n2- photograph close up portrait old tough decorated general, serious, stoic cinematic 4k epic detailed 4k epic detailed photograph shot on kodak detailed bokeh cinematic hbo dark moody \n3- photorealistic young mother walking at the beach, holding hands with her little son, mountains in the background, photography style, 85mm bookeh detailed, high resolution, high quality, natural lighting, ultra-detailed \n4-Landscape photography of snow-covered mountain peaks at sunrise, using natural light. \n5-Portrait photography during the golden hour, using the soft, warm light to highlight the subject."
        prompt_user2 = "Write in english an image prompt in the same format as the examples, capable of generating an image on the content below : \n"
        prompt_user2 += subject
        prompt_user2 += "\n"
        prompt_user2 += content
        prompt_user2 += "\n\nThe size and content of the image must respect the "
        prompt_user2 += network
        prompt_user2 += " formalism. Write only the image prompt, do not add emoji or hashtags."

    if language == Language.FRENCH.value:
        prompt_system2 = "Vous êtes un ingénieur des prompts, spécialisé dans les prompts de génération d'images. Voici quelques examples de prompts:\n1- Woman, beautiful bedroom, glasses, showing skin, soft symmetric facial features, close up portrait, young, shot on sony a1, 85mm F/1. 4 ISO 100, medium format, 45 megapixel, flash lighting, natural sun lighting \n2- photograph close up portrait old tough decorated general, serious, stoic cinematic 4k epic detailed 4k epic detailed photograph shot on kodak detailed bokeh cinematic hbo dark moody \n3- photorealistic young mother walking at the beach, holding hands with her little son, mountains in the background, photography style, 85mm bookeh detailed, high resolution, high quality, natural lighting, ultra-detailed \n4-Landscape photography of snow-covered mountain peaks at sunrise, using natural light. \n5-Portrait photography during the golden hour, using the soft, warm light to highlight the subject."
        prompt_user2 = "Ecrivez en anglais un prompt de génération d'image dans le même format que les exemples, capable de générer une image sur le contenu suivant: \n"
        prompt_user2 += subject
        prompt_user2 += "\n"
        prompt_user2 += content
        prompt_user2 += "\n\nLa taille et le contenu de l'image devront respecter le formalisme du réseau social "
        prompt_user2 += network
        prompt_user2 += ". Ecrivez seulement le prompt pour générer l'image, n'ajoutez pas d'émoji ou de hashtags."

    image_prompt = askOpenAI(prompt_user2, prompt_system2)

    decrement_text_credit(id_user)

    return {
        "network": network,
        "text": post_text,
        "prompt_image": image_prompt,
        "text_credit": user["text_credit"] - 1,
    }


class ImageSchema(BaseModel):
    network: str
    image_prompt: str

#route
@router_gen.post("/content/image")
async def create_content_image(image_schema: ImageSchema, authorization=Header(None)):
    jwt_token = authorization.split("Bearer ")[1]
    if not jwt_token:
        raise NotAuthError({"message": "No token provided"})
    decoded_payload = jwt.decode(jwt_token, KEY, algorithms=["HS256"])
    email = decoded_payload.get("email")
    user = get(email)
    id_user = user["id"]

    if user["image_credit"] == 0:
        raise GeneratingError({"message": "No credit left"})

    network = image_schema.network
    image_prompt = image_schema.image_prompt

    image_url_1 = drawDalle3(image_prompt, network)
    image_url_2 = drawDalle3(image_prompt, network)
    image_url_3 = drawDalle3(image_prompt, network)
    image_url_4 = drawDalle3(image_prompt, network)
    images = [
        {"id": "a", "url": image_url_1},
        {"id": "b", "url": image_url_2},
        {"id": "c", "url": image_url_3},
        {"id": "d", "url": image_url_4},
    ]

    decrement_image_credit(id_user)

    return {
        "network": network,
        "images": images,
        "image_credit": user["image_credit"] - 1,
    }
