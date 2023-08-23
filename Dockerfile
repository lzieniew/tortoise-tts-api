# Python 3.10 w/ Nvidia Cuda
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04 AS env_base

# Install Pre-reqs
RUN apt-get update && apt-get install --no-install-recommends -y \
    git vim nano build-essential python3-dev python3-venv python3-pip gcc g++ ffmpeg

# Setup venv
RUN pip3 install virtualenv
RUN virtualenv /venv
ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip3 install --upgrade pip setuptools && \
    pip3 install torch torchvision torchaudio

## Set working directory
#WORKDIR /app
#
## Clone the repo
#RUN git clone https://github.com/rsxdalv/tts-generation-webui.git
#
## Set working directory to the cloned repo
#WORKDIR /app/tts-generation-webui

# 2. Copy files
COPY . /src

WORKDIR /src

# Install all requirements
RUN pip install torch==1.12.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip3 install -r requirements.txt
#RUN pip3 install -r requirements_audiocraft.txt
#RUN pip3 install -r requirements_bark_hubert_quantizer.txt
#RUN pip3 install -r requirements_rvc.txt
RUN pip3 install deepspeed==0.8.3

RUN python3 setup.py install

CMD ["uvicorn", "rest_api:app", "--host", "0.0.0.0", "--port", "5000"]
