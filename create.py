import os
import sys
import json
import openai
import requests
from secret import *

def makeScript(prompt):

    addition = "Return five paragraphs of text where the topic is"

    # 2 Prompt to script with chatGPT API
    openai.api_key = api_key_chat_gpt

    URL = "https://api.openai.com/v1/chat/completions"

    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"{addition} {prompt}"}]
    }
    r = requests.post(URL, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key_chat_gpt}"
        }, 
        json = body
    )

    data = r.json()

    script = data["choices"][0]["message"]["content"]

    return script

def makeAudio(script):
    # 3 Voice the script with Eleven Labs API
    josh_voice_id = "TxGEqnHWrfWFTfGW9XjX"
    labs_url = f"https://api.elevenlabs.io/v1/text-to-speech/{josh_voice_id}"

    api_key_eleven_labs

    body = {
    "text": script,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.75,
        "similarity_boost": 0.75
    }
    }

    r = requests.post(labs_url, headers={
            "xi-api-key": api_key_eleven_labs
        }, 
        json = body
    )

    with open("output.mp3", "wb") as file:
        file.write(r.content)

def makeVideo():
    # 4 Create video with ffmpeg (combine audio and thumbnail png)
    os.system("ffmpeg -loop 1 -i logo.png -i output.mp3 -shortest -acodec copy -vcodec mjpeg out.mkv")

def uploadYouTube():
    # 5 Upload to YouTube
    pass

def main():
    
    prompt = sys.argv[1]

    script = makeScript(prompt)
    
    makeAudio(script)
    
    makeVideo()

main()