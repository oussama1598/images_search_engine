import logging


class Logger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)

        self.setLevel(logging.DEBUG)

        log_stream = logging.StreamHandler()
        log_stream.setLevel(logging.DEBUG)
        log_stream.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        )

        self.addHandler(log_stream)
