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
    "text": "Listen to this flow:",
    "voice_description": "In the game of rhymes, I'm the undisputed champ, lyrics so hot they'll leave your speakers damp. My flow's smooth like butter, words sharp as a razor, spittin' verses that'll make you a true hip-hop praiser. From the streets to the beats, I'm always on the grind, leaving wack MCs far behind in my rhyme design."
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
