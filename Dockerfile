FROM python:3.9

WORKDIR /check-design

COPY src /check-design/src
COPY requirements.txt /check-design/requirements.txt

RUN ls /check-design -la
RUN pip3 install --no-cache-dir -r /check-design/requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install tesseract-ocr libtesseract-dev -y

ENTRYPOINT [ "python3" , "-m", "src"]
