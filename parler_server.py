"""
Project: Parler-TTS-FastAPI
Author: ParisNeo (Research Engineer)
Version: 1.1
Description: 
This project implements a FastAPI-based web service for the Parler-TTS (Text-to-Speech) model.
It provides endpoints for generating speech from text input, supporting both single-request
and streaming responses. The API can output audio in base64 encoded format or as WAV files.
It's designed to run on either CPU or GPU, offering flexibility for different deployment scenarios.

Key Features:
- Text-to-speech generation with customizable voice descriptions
- Streaming capability for processing longer texts
- Support for base64 and WAV output formats
- GPU acceleration support
- Sentence-by-sentence processing for streaming responses

This API serves as a powerful tool for integrating high-quality text-to-speech capabilities
into various applications, from voice assistants to accessibility tools.
"""
import argparse
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import io
import base64
import nltk
from typing import List, Optional
from enum import Enum

description = """
Parler-TTS API

This API provides text-to-speech generation using the Parler-TTS model. It offers two main endpoints:

1. /generate_speech: Generates speech for a given text and voice description.
2. /generate_speech_stream: Streams generated speech for longer texts, processing sentence by sentence.

Both endpoints support output in base64 encoded format or as WAV files.

The API can be configured to run on a specific host and port, and can utilize GPU acceleration if available.
"""

nltk.download('punkt')

class OutputFormat(str, Enum):
    base64 = "base64"
    wav = "wav"

class TTSRequest(BaseModel):
    text: str
    voice_description: str
    output_format: Optional[OutputFormat] = OutputFormat.base64

class TTSResponse(BaseModel):
    audio: str  # Base64 encoded WAV file or "WAV file generated" message

app = FastAPI(title="Parler-TTS API", description=description)

def generate_audio_chunk(text: str, voice_description: str) -> bytes:
    input_ids = tokenizer(voice_description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(text, return_tensors="pt").input_ids.to(device)

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()

    buffer = io.BytesIO()
    sf.write(buffer, audio_arr, model.config.sampling_rate, format='wav')
    buffer.seek(0)
    return buffer.getvalue()

@app.post("/generate_speech", response_model=TTSResponse)
async def generate_speech(request: TTSRequest):
    """
    Generate speech from the given text and voice description.

    This endpoint takes a text input and a voice description, generates the corresponding
    speech using the Parler-TTS model, and returns the audio data.

    Parameters:
    - request (TTSRequest): An object containing the following fields:
        - text (str): The text to be converted to speech.
        - voice_description (str): A description of the desired voice characteristics.
        - output_format (OutputFormat, optional): The desired output format (base64 or wav).
          Defaults to base64.

    Returns:
    - TTSResponse: An object containing the generated audio data.
        If output_format is base64, the audio field will contain a base64 encoded string.
        If output_format is wav, a WAV file will be returned directly.

    Raises:
    - HTTPException: If there's an error during speech generation.
    """
    try:
        audio_data = generate_audio_chunk(request.text, request.voice_description)
        
        if request.output_format == OutputFormat.base64:
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            return TTSResponse(audio=audio_base64)
        else:
            return Response(content=audio_data, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_speech_stream")
async def generate_speech_stream(
    request: TTSRequest,
    output_format: OutputFormat = Query(OutputFormat.base64, description="Output format: base64 or wav")
):
    """
    Stream generated speech from the given text and voice description.

    This endpoint takes a text input and a voice description, generates the corresponding
    speech using the Parler-TTS model, and streams the audio data sentence by sentence.

    Parameters:
    - request (TTSRequest): An object containing the following fields:
        - text (str): The text to be converted to speech.
        - voice_description (str): A description of the desired voice characteristics.
    - output_format (OutputFormat, optional): The desired output format (base64 or wav).
      Defaults to base64.

    Returns:
    - StreamingResponse: A streaming response containing the generated audio data.
        If output_format is base64, each chunk will be a base64 encoded string followed by a newline.
        If output_format is wav, raw audio data will be streamed.

    Raises:
    - HTTPException: If there's an error during speech generation.
    """
    try:
        sentences = nltk.sent_tokenize(request.voice_description)
        
        if output_format == OutputFormat.base64:
            async def generate():
                for sentence in sentences:
                    audio_chunk = generate_audio_chunk(request.text, sentence)
                    yield base64.b64encode(audio_chunk) + b'\n'
            
            return StreamingResponse(generate(), media_type="text/plain")
        else:
            async def generate():
                for sentence in sentences:
                    audio_chunk = generate_audio_chunk(request.text, sentence)
                    yield audio_chunk
            
            return StreamingResponse(generate(), media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """
    Root endpoint that provides a welcome message.

    Returns:
    - dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to the Parler-TTS API"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=8593, help='Port to run the server on')
    parser.add_argument('--use-cpu', action='store_true', help='Use CPU for inference instead of GPU')
    args = parser.parse_args()

    if not args.use_cpu and torch.cuda.is_available():
        device = "cuda:0"
        print("Using GPU for inference.")
    else:
        device = "cpu"
        print("Using CPU for inference.")

    # Load model and tokenizer
    model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-v1").to(device)
    tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")

    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port)
