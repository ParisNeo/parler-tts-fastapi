from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import io
import base64
import nltk
from typing import List

nltk.download('punkt')

app = FastAPI(title="Parler-TTS API", description="API for text-to-speech generation using Parler-TTS")

# Load model and tokenizer
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-v1").to(device)
tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")

class TTSRequest(BaseModel):
    prompt: str
    description: str

class TTSResponse(BaseModel):
    audio: str  # Base64 encoded WAV file

def generate_audio_chunk(prompt: str, description: str) -> bytes:
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()

    buffer = io.BytesIO()
    sf.write(buffer, audio_arr, model.config.sampling_rate, format='wav')
    buffer.seek(0)
    return buffer.getvalue()

@app.post("/generate_speech", response_model=TTSResponse)
async def generate_speech(request: TTSRequest):
    try:
        audio_data = generate_audio_chunk(request.prompt, request.description)
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        return TTSResponse(audio=audio_base64)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_speech_stream")
async def generate_speech_stream(request: TTSRequest):
    try:
        sentences = nltk.sent_tokenize(request.description)
        
        async def generate():
            for sentence in sentences:
                audio_chunk = generate_audio_chunk(request.prompt, sentence)
                yield audio_chunk
        
        return StreamingResponse(generate(), media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the Parler-TTS API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8593)
