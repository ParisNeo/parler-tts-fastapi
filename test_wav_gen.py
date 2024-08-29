import requests
import base64

url = "http://localhost:8593/generate_speech"

data = {
    "text": "Hi my lover. I want you to make me moan.",
    "voice_description": "Alisson, a hot chick with hot voice"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    audio_base64 = response.json()['audio']
    audio_data = base64.b64decode(audio_base64)
    
    # Save the audio file
    with open("rap_verse.wav", "wb") as f:
        f.write(audio_data)
    print("Audio saved as rap_verse.wav")
else:
    print(f"Error: {response.status_code}, {response.text}")