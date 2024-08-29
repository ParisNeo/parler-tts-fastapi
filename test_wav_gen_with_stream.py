import requests

url = "http://localhost:8593/generate_speech_stream"

data = {
    "text": "Listen up: this is a rap song, from a mat mong. giving a black dong. In a shot shong.",
    "voice_description": "From the streets to the beats, I'm rising up like heat. Got rhymes so sweet, they'll sweep you off your feet. My lyrics are elite, can't compete with this treat. I'm dropping bars like they're obsolete, complete with a rhythmic heartbeat."
}

response = requests.post(url, json=data, stream=True)

if response.status_code == 200:
    # Save the streamed audio
    with open("streamed_rap.wav", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Streamed audio saved as streamed_rap.wav")
else:
    print(f"Error: {response.status_code}, {response.text}")
