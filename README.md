# Parler-TTS FastAPI Server

This project provides a FastAPI server for the Parler-TTS library, allowing users to generate speech from text using the Parler-TTS model via HTTP requests.

## Features

- Text-to-speech generation using Parler-TTS
- FastAPI server with Swagger UI documentation
- Base64 encoded WAV file output

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- PyTorch
- Parler-TTS
- Transformers
- SoundFile
- Pydantic

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/parler-tts-server.git
   cd parler-tts-server
   ```

2. Install the required dependencies:
   ```
   pip install fastapi uvicorn pydantic soundfile torch transformers parler-tts
   ```

## Usage

1. Start the server:
   ```
   python parler_tts_server.py
   ```

2. The server will start running on `http://localhost:8000`.

3. Access the API documentation at `http://localhost:8000/docs`.

4. To generate speech, send a POST request to `http://localhost:8000/generate_speech` with a JSON body:
   ```json
   {
     "prompt": "Hey, how are you doing today?",
     "description": "A female speaker delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up."
   }
   ```

5. The API will respond with a JSON object containing the base64-encoded WAV file of the generated speech.

## API Endpoints

### POST /generate_speech

Generates speech from the given prompt and description.

**Request Body:**

- `prompt` (string): The text to be converted to speech.
- `description` (string): A description of the desired speech characteristics.

**Response:**

- `audio` (string): Base64 encoded WAV file of the generated speech.

### GET /

Returns a welcome message.

## Error Handling

The server includes basic error handling. If an error occurs during speech generation, it will return a 500 Internal Server Error with details about the error.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgements

This project uses the Parler-TTS model. Please refer to the [Parler-TTS repository](https://github.com/parler-tts/parler-tts) for more information about the model and its license.
