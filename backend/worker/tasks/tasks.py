import asyncio
import io
import json
import logging
import os

from transformers import pipeline
import torch
import torchaudio
import numpy as np

from app.database import DatabaseSessionManager
from app.models import Job
from app.models.results import WhisperResult, KeyWordsResult
from fastapi_storages import FileSystemStorage

# from .front_extraction import parse_file
# from .keywords_pipe import get_keywords
# from .llm_test import get_model_and_tokenizer, get_key_stage2_llm
# from .keywords_filter import filter_text
from ..app import app

@app.task(
    # autoretry_for=(Exception,), retry_backoff=True, retry_backoff_max=1800, max_retries=5
)
def whisper_task(job_id: str):
    storage = FileSystemStorage(path="/tmp")
    with DatabaseSessionManager() as db_session:
        job = db_session.query(Job).get(job_id)
    file_path = "/opt/app" + storage.get_path(job.audio_file)

    DEVICE = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    logging.info(f'{DEVICE} {torch.cuda.is_available()}')

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

    logging.info(f'File name {file_path}')

    # with open(file_path, "rb") as f:
    #     audio_file = io.BytesIO(f.read())
    logging.info(f"{torchaudio.get_audio_backend()}")
    waveform, sr = torchaudio.load(file_path)
    waveform = torchaudio.functional.resample(waveform, orig_freq=sr, new_freq=16000)
    waveform = np.mean(waveform.numpy(), axis=0)

    prediction_json = pipe(waveform, batch_size=6)
    del pipe

    with DatabaseSessionManager() as db_session:
        whisper_result = WhisperResult(job_id=job_id, text=json.dumps(prediction_json))
        whisper_result.save_sync(db_session)
        job.status = "whisper_done"
        job.save_sync(db_session)
    get_result(job_id)
    return prediction_json

@app.task(
    # autoretry_for=(Exception,), retry_backoff=True, retry_backoff_max=1800, max_retries=5
)
def get_result(job_id: str, keywords: list = None):
    from .front_extraction import parse_file
    from .keywords_pipe import get_keywords
    from .keywords_filter import filter_text
    from .llm_test import get_model_and_tokenizer, get_key_stage2_llm

    with DatabaseSessionManager() as db_session:
        job = db_session.query(Job).get(job_id)
        all_key_words, description = get_keywords(json.loads(job.whisper_result.text)['text'], '', '/opt/app')

    keywords_filtered, english_words = filter_text(json.loads(job.whisper_result.text), keywords, "/opt/app")

    model_llm, tokenizer_llm, device = get_model_and_tokenizer()
    final_keywords = get_key_stage2_llm(keywords_filtered, job.whisper_result.text, model_llm, tokenizer_llm, device, "f")
    final_keywords = [w.capitalize() for w in final_keywords]

    result = parse_file(job.whisper_result.text, description)

    with DatabaseSessionManager() as db_session:
        job = db_session.query(Job).get(job_id)
        keywords_result = KeyWordsResult(job_id=job_id, keywords=json.dumps(result))
        keywords_result.save_sync(db_session)
        job.status = "completed"
        job.save_sync(db_session)
    return result
