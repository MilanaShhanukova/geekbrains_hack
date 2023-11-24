import whisperx
import torch
import argparse
import glob
import os
import json
from tqdm import tqdm
import os

from transformers import WhisperForConditionalGeneration, WhisperProcessor
from transformers import pipeline
import torch
import torchaudio
import numpy as np
import json


compute_type = "float32"
device = "cuda:0" if torch.cuda.is_available() else "cpu"


def transcibe_audio(audio_file: str, model, batch_size, model_type="whisperx"):
    if model_type == "whisperx":
        audio_part = whisperx.load_audio(audio_file)
        result = model.transcribe(audio_part, batch_size=batch_size)
    elif model_type == "whisper":
        waveform, sr = torchaudio.load(audio_file)
        waveform = torchaudio.functional.resample(
            waveform, orig_freq=sr, new_freq=16000
        )
        waveform = np.mean(waveform.numpy(), axis=0)

        result = model(waveform, batch_size=6)

    return result


def transribe_pipeline(
    files_folder: str, texts_dir: str, batch_size: int, model, model_type
):
    audio_paths_mp3 = list(glob.iglob(f"{files_folder}/*.mp3"))
    audio_paths_wav = list(glob.iglob(f"{files_folder}/*.wav"))

    for f_path in tqdm(audio_paths_mp3 + audio_paths_wav):
        transcibed_result = transcibe_audio(f_path, model, batch_size, model_type)

        file_name = f_path.split("/")[-1][:-4]

        with open(
            os.path.join(texts_dir, file_name + ".json"), "w+", encoding="utf-8"
        ) as outfile:
            json.dump(transcibed_result, outfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Parse the audio files")
    parser.add_argument("--folder_audio_path", default="./train_data/audiofiles")
    parser.add_argument("--folder_text_path", default="./train_data/textfiles/raw")
    parser.add_argument("--batch_size", default=8)
    parser.add_argument("--model_type", default="whisperx")

    parsed_args = parser.parse_args()

    if parsed_args.model_type == "whisperx":
        model = whisperx.load_model("large-v2", device, compute_type=compute_type)
    elif parsed_args.model_type == "whisper":
        model = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-large-v3",
            chunk_length_s=30,
            device=device,
            return_timestamps=True,
        )

    if not os.path.exists(parsed_args.folder_text_path):
        os.makedirs(parsed_args.folder_text_path)

    transribe_pipeline(
        parsed_args.folder_audio_path,
        parsed_args.folder_text_path,
        parsed_args.batch_size,
        model,
        parsed_args.model_type,
    )
