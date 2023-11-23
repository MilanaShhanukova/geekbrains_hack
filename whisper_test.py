import os

from transformers import WhisperForConditionalGeneration, WhisperProcessor
from transformers import pipeline
import torch
import torchaudio
import numpy as np
import json

DEVICE = 'cuda:0' if torch.cuda.is_available() else 'cpu'

processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3").to(device=DEVICE)

for audio_name in os.listdir('train_data/audiofiles/'):
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-large-v3",
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