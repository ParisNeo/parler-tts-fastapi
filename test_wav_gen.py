import requests
import base64

url = "http://localhost:8593/generate_speech"

data = {
    "text": "From the streets to the beats, I'm rising up like heat. Got rhymes so sweet, they'll sweep you off your feet. My lyrics are elite, can't compete with this treat. I'm dropping bars like they're obsolete, complete with a rhythmic heartbeat.",
    "voice_description": "male rapper voice. Groovy."
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
