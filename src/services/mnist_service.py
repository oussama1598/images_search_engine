import numpy as np

from src.modules.mnist_engine import MnistEngine
from src.settings import settings

mnist_engine = MnistEngine(
    encoder_path=settings.MNIST_ENCODER_PATH,
    decoder_path=settings.MNIST_DECODER_PATH
)


def get_image_neighbors(encoded_image: np.array, neighbors: int = 10):
    neighbors = np.array([np.array(embedding) for embedding in mnist_engine.get_neighbors(encoded_image, neighbors)])

    return [
        image.reshape(28, 28) * 255
        for image in mnist_engine.decode_images(neighbors)
    ]


def encode_image(image: np.array):
    return mnist_engine.encode_images(np.array([image]))
