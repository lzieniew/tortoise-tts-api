docker run -v ./results:/src/results --gpus all -it tortoise /bin/bash

python tortoise/do_tts.py --text "I'm going to speak this" --voice snakes --preset ultra_fast


from tortoise.api import TextToSpeech
tts = TextToSpeech(half=True, kv_cache=True, enable_redaction=True)
tts.tts_with_preset("I'm a voice generated in python", preset='ultra_fast')
