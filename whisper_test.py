import os

from transformers import WhisperForConditionalGeneration, WhisperProcessor
from transformers import pipeline
import torch
import torchaudio
import numpy as np
import json

def process_file_whisper(path):
    # local cached file, non-docker run
    if os.path.exists('backend/docker/models/whisper-large-v3/'):
        repo_path = "backend/docker/models/whisper-large-v3/"
    # docker run
    elif os.path.exists('models/whisper-large-v3/'):
        repo_path = "models/whisper-large-v3/"
    # default to huggingface hub download
    else:
        repo_path = "openai/whisper-large-v3"

    pipe = pipeline(
        "automatic-speech-recognition",
        model=repo_path,
        chunk_length_s=30,
        device=DEVICE,
        return_timestamps=True,
    )

    print(path)
    waveform, sr = torchaudio.load(path)
    waveform = torchaudio.functional.resample(waveform, orig_freq=sr, new_freq=16000)
    waveform = np.mean(waveform.numpy(), axis=0)
    print(f'audio len for {path}: {waveform.shape[0] // 16000} sec')
    # debug
    # waveform = waveform[16000*60*4:16000*60*5]

    prediction = pipe(waveform, batch_size=6)
    #with open(f'{str.split(audio_name, ".")[0]}.json', 'w', encoding='utf-8') as jsf:
    #    json.dump(prediction, jsf, ensure_ascii=False, indent=4)
    print(prediction)
    del pipe
    return prediction

DEVICE = 'cuda:0' if torch.cuda.is_available() else 'cpu'

#processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3")
#model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3", use_flash_attention_2=True).to(device=DEVICE)

if __name__ == '__main__':
    # local cached file, non-docker run
    if os.path.exists('backend/docker/models/whisper-large-v3/'):
        repo_path = "backend/docker/models/whisper-large-v3/"
    # docker run
    elif os.path.exists('models/whisper-large-v3/'):
        repo_path = "models/whisper-large-v3/"
    # default to huggingface hub download
    else:
        repo_path = "openai/whisper-large-v3"

    print(f'Loading Whisper from {repo_path}')

    for audio_name in os.listdir('train_data/audiofiles/'):
        pipe = pipeline(
            "automatic-speech-recognition",
            model=repo_path,
            chunk_length_s=30,
            device=DEVICE,
            return_timestamps=True,
        )
        print(audio_name)
        waveform, sr = torchaudio.load(f'train_data/audiofiles/{audio_name}')
        waveform = torchaudio.functional.resample(waveform, orig_freq=sr, new_freq=16000)
        waveform = np.mean(waveform.numpy(), axis=0)
        # debug
        # waveform = waveform[16000*60*4:16000*60*5]

        prediction = pipe(waveform, batch_size=6)
        with open(f'{str.split(audio_name, ".")[0]}.json', 'w', encoding='utf-8') as jsf:
            json.dump(prediction, jsf, ensure_ascii=False, indent=4)
        print(prediction)