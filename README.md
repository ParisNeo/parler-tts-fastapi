# Parler-TTS-FastAPI

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0%2B-green)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)
![Version](https://img.shields.io/badge/Version-1.1-brightgreen)
[![GitHub issues](https://img.shields.io/github/issues/ParisNeo/parler-tts-fastapi)](https://github.com/ParisNeo/parler-tts-fastapi/issues)
[![GitHub stars](https://img.shields.io/github/stars/ParisNeo/parler-tts-fastapi)](https://github.com/ParisNeo/parler-tts-fastapi/stargazers)

## Project Overview
- **Author**: ParisNeo (Research Engineer)
- **Version**: 1.1
- **Description**: This project implements a FastAPI-based web service for the Parler-TTS (Text-to-Speech) model. It provides endpoints for generating speech from text input, supporting both single-request and streaming responses. The API can output audio in base64 encoded format or as WAV files.

## Key Features
- Text-to-speech generation with customizable voice descriptions
- Streaming capability for processing longer texts
- Support for base64 and WAV output formats
- GPU acceleration support
- Sentence-by-sentence processing for streaming responses
- FastAPI server with automatic Swagger UI documentation

## Requirements
- Python 3.7+
- FastAPI
- Uvicorn
- PyTorch
- Parler-TTS
- Transformers
- SoundFile
- Pydantic
- NLTK

## Installation

1. Install PyTorch with CUDA support (if available):
   ```
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --upgrade
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:
   ```
   python parler_tts_server.py [--host HOST] [--port PORT] [--use-gpu]
   ```
   
   Options:
   - `--host`: Host to run the server on (default: 0.0.0.0)
   - `--port`: Port to run the server on (default: 8593)
   - `--use-gpu`: Use GPU for inference if available

2. The server will start running on the specified host and port (default: `http://0.0.0.0:8593`).

3. Access the API documentation at `http://<host>:<port>/docs`.

## API Endpoints

### POST /generate_speech

Generates speech from the given text and voice description.

**Request Body:**
```json
{
  "text": "Hello, how are you?",
  "voice_description": "A friendly, warm female voice",
  "output_format": "base64"
}
```

**Response:**
- Base64 encoded WAV file or WAV file directly, depending on the specified output format.

### POST /generate_speech_stream

Streams generated speech for longer texts, processing sentence by sentence.

**Request Body:**
Same as `/generate_speech`

**Response:**
- Streaming response with audio data in the specified format.

### GET /

Returns a welcome message.

## Error Handling

The server includes error handling. If an error occurs during speech generation, it will return a 500 Internal Server Error with details about the error.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache 2.0 License.

## Acknowledgements

This project uses the Parler-TTS model. Please refer to the [Parler-TTS repository](https://github.com/parler-tts/parler-tts) for more information about the model and its license.
