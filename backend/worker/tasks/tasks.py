import asyncio
import logging
import os
from uuid import UUID

from transformers import pipeline
import torch
import torchaudio
import numpy as np

from app.database import get_db
from app.models.results import WhisperResult
from ..app import app

@app.task(autoretry_for=(Exception,), retry_backoff=True, retry_backoff_max=1800, max_retries=5)
def whisper_task(audio_file: str, job_id: UUID):
    DEVICE = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    # local cached file, non-docker run
    if os.path.exists('backend/docker/models/whisper-large-v3/'):
        repo_path = "backend/docker/models/whisper-large-v3/"
    # docker run
    elif os.path.exists('models/whisper-large-v3/'):
        repo_path = "models/whisper-large-v3/"
    # default to huggingface hub download
    else:
        repo_path = "openai/whisper-large-v3"

    logging.info(f'Loading Whisper from {repo_path}')

    pipe = pipeline(
        "automatic-speech-recognition",
        model=repo_path,
        chunk_length_s=30,
        device=DEVICE,
        return_timestamps=True,
    )

    logging.info(f'File name {audio_file}')

    waveform, sr = torchaudio.load(f'train_data/audiofiles/{audio_name}')
    waveform = torchaudio.functional.resample(waveform, orig_freq=sr, new_freq=16000)
    waveform = np.mean(waveform.numpy(), axis=0)

    prediction_json = pipe(waveform, batch_size=6)

    async def save_to_db():
        async with get_db() as session:
            whisper_result = WhisperResult(job_id=job_id, text=prediction_json)
            await whisper_result.save(session)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(save_to_db())

    return prediction_json

