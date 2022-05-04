import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str

    MNIST_ENCODER_PATH: str = os.path.join(os.getcwd(), './src/models/mnist/encoder.h5')
    MNIST_DECODER_PATH: str = os.path.join(os.getcwd(), './src/models/mnist/decoder.h5')

    class Config:
        env_file = "../.env"


settings = Settings()
