import os

import numpy as np
from keras.datasets import mnist

from src.db import cassandra_db
from src.modules.mnist_engine import MnistEngine


def generate_embeddings():
    (x_train, _), (x_test, _) = mnist.load_data()
    x = np.vstack([x_train, x_train])

    x = x.astype('float32') / 255.
    x = np.reshape(x, (len(x), 28, 28, 1))

    mnist_engine = MnistEngine(
        os.path.join(os.getcwd(), './src/models/mnist/encoder.h5'),
        os.path.join(os.getcwd(), './src/models/mnist/encoder.h5')
    )

    return mnist_engine.encode_images(x)


if __name__ == '__main__':
    session = cassandra_db.get_session()

    session.execute('DROP TABLE IF EXISTS mnist.embeddings;')
    session.execute('CREATE TABLE mnist.embeddings(img_id int PRIMARY KEY, embedding list<double>);')

    prepared_query = session.prepare('INSERT INTO mnist.embeddings (img_id, embedding) values (?, ?)')
    embeddings = generate_embeddings()

    for i, embedding in enumerate(embeddings):
        session.execute(prepared_query, (i, embedding))
