import requests
import numpy as np
import sounddevice as sd
import time
import sys
# Audio setup
sample_rate = 22050  # Parler-TTS default sample rate
dtype = np.int16

def audio_callback(outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    global audio_buffer
    if len(audio_buffer) < frames * 2:
        outdata[:] = 0
        raise sd.CallbackStop()
    else:
        outdata[:] = np.frombuffer(audio_buffer[:frames*2], dtype=dtype).reshape(-1, 1)
        audio_buffer = audio_buffer[frames*2:]

url = "http://localhost:8593/generate_speech_stream"

data = {
    "text": "From the streets to the beats, I'm rising up like heat. Got rhymes so sweet, they'll sweep you off your feet. My lyrics are elite, can't compete with this treat. I'm dropping bars like they're obsolete, complete with a rhythmic heartbeat.",
    "voice_description": "male rapper voice. Groovy."
}

response = requests.post(url, json=data, stream=True)

if response.status_code == 200:
    print("Starting playback...")
    
    audio_buffer = b""
    stream = sd.OutputStream(samplerate=sample_rate, channels=1, callback=audio_callback, dtype=dtype)
    
    with stream:
        for chunk in response.iter_content(chunk_size=1024):
            audio_buffer += chunk
            if len(audio_buffer) >= 4096:  # Start playback when we have enough data
                stream.start()
            time.sleep(0.01)  # Small delay to prevent buffer overflow
    
    print("Playback finished")
else:
    print(f"Error: {response.status_code}, {response.text}")
