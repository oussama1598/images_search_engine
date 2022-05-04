FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN mkdir /code/backend

COPY ./src /code/backend/src
COPY ./main.py /code/backend/main.py
COPY ./.env /code/backend/.env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
