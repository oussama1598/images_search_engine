import numpy as np
import pandas as pd
from tensorflow import keras

from backend.src.db import cassandra_db
from backend.src.modules.logger import Logger


class MnistEngine:
    def __init__(self, encoder_path: str, decoder_path: str):
        self.encoder = keras.models.load_model(encoder_path)
        self.decoder = keras.models.load_model(decoder_path)

        self.embeddings = []
        self.logger = Logger('MNIST-ENGINE')
        self.cassandra_session = cassandra_db.get_session()

        self.__init_cassandra_distance_function()

    def __init_cassandra_distance_function(self):
        self.logger.info('Adding distance function to cassandra.')

        self.cassandra_session.execute('DROP FUNCTION IF EXISTS mnist.euclidean;')
        self.cassandra_session.execute("CREATE FUNCTION mnist.euclidean(source list<double>, target list<double>)"
                                       "CALLED ON NULL INPUT RETURNS double LANGUAGE java AS '"
                                       "double  distance = 0;"
                                       "for (int i=0;i<source.size();i++){"
                                       "    double p = source.get(i);"
                                       "    double q = target.get(i);"
                                       "    distance = distance + (p - q) * (p - q);"
                                       "}"
                                       "distance = java.lang.Math.sqrt(distance);"
                                       "return distance;"
                                       "';"
                                       )

    def encode_images(self, images: np.array):
        return self.encoder.predict(images)

    def decode_images(self, images: np.array):
        return self.decoder.predict(images)

    def get_neighbors(self, encoded_image: np.array, neighbors: int = 10):
        rows = list(self.cassandra_session.execute(
            'SELECT embedding, mnist.euclidean(embedding, %s) as distance FROM mnist.embeddings' % (
                encoded_image.tolist())))

        df = pd.DataFrame(rows, columns=['embedding', 'distance'])

        return df.sort_values(by=['distance']).reset_index(drop=True)['embedding'][:neighbors]
