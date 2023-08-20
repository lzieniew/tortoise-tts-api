from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class TTSRequest(BaseModel):
    sentence: str
    engine: str = 'tortoise'


@app.post("/tts/")
async def text_to_speech(data: TTSRequest):
    sentence = data.sentence
    tts_engine = data.engine

    if not sentence:
        raise HTTPException(status_code=400, detail="Please provide a sentence.")
    
    # Instead of processing through TTS, just return the same text
    return {"text": sentence}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

