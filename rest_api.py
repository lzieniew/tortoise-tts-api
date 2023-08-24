import io

import torchaudio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from tortoise.utils import audio
from tortoise import api

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

TTS = api.TextToSpeech(kv_cache=True, half=True, use_Deepspeed=True)

def generate_text(sentence: str):
    global TTS
    clips_paths = [
        '/src/tortoise/voices/train_empire/1.mp3',
        '/src/tortoise/voices/train_empire/2.mp3',
        '/src/tortoise/voices/train_empire/3.mp3',
    ]
    reference_clips = [audio.load_audio(p, 22050) for p in clips_paths]
    audio_output = TTS.tts_with_preset(sentence, voice_samples=reference_clips, preset='ultra_fast')
    buffer = io.BytesIO()
    torchaudio.save(buffer, audio_output.squeeze(0).cpu(), format="wav", sample_rate=24000)
    buffer.seek(0)

    # Return the audio data as a streaming response
    return buffer


class TTSRequest(BaseModel):
    sentence: str
    engine: str = 'tortoise'


@app.post("/tts/")
@app.post("/tts")
async def text_to_speech(data: TTSRequest):
    sentence = data.sentence
    tts_engine = data.engine

    if not sentence:
        raise HTTPException(status_code=400, detail="Please provide a sentence.")

    buffer = generate_text(sentence)

    return StreamingResponse(buffer, media_type="audio/wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
