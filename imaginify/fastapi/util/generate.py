import os
import requests

from openai import AzureOpenAI, OpenAI

# ------------------- CONFIG OPENAI ------------------- #
client = AzureOpenAI(
    azure_deployment="FujiOpenAiDeploy",
    azure_endpoint="https://fujitsu-openai.openai.azure.com",
    api_key=os.getenv("OPENAI_API_KEY"), #c0bd9c7bf2ab4f82a2d070aa6212e9a3
    api_version="2023-05-15"
)

draw = OpenAI(
    api_key= "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",
    organization="org-2aLBjgtPwWhnFgcgdp8trmFJ"
)
# ----------------------------------------------------- #



def askOpenAI(user_prompt, system_prompt):

    response = client.chat.completions.create(
        model = "FujiOpenAiDeploy", 
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature = 0.9,
    )

    return response.choices[0].message.content

def drawDalle3(prompt, network) : 

    size = "1024x1024"

    if (network == "Instagram") :
        size = "1024x1792"
    if (network == "Blog") :
        size = "1792x1024"
    
    url = "https://api.openai.com/v1/images/generations"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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',
        'OpenAI-Organization': 'org-2aLBjgtPwWhnFgcgdp8trmFJ'
    }

    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size
    }

    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        
        data = response.json()
        generated_url = data['data'][0]['url']

        return generated_url

    except requests.exceptions.RequestException as err:
        print("An error occured while generateing the images : ", err)
