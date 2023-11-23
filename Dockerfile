FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

RUN apt-get update -y
RUN apt-get install -y python3-pip build-essential
RUN apt-get install -y git
# RUN apt-get install -y ffmpeg

RUN pip3 install torch==2.1.0+cu118 torchvision==0.16.0+cu118 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118

COPY requirements.txt /
RUN pip3 install packaging
RUN pip3 install -r requirements.txt

COPY train_data/audiofiles train_data/audiofiles
COPY *.py /
COPY *.json /

USER root
WORKDIR /

# docker build -t fttftf_1:test .
# docker run --gpus all -it fttftf_1:test bin/bash