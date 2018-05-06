import logging
import sys


def configure(logger: logging.Logger = logging.root):
    class InfoFilter(logging.Filter):
        def filter(self, rec):
            return rec.levelno in (logging.DEBUG, logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s", "%d/%m/%Y %H:%M:%S")

    std_out_handler = logging.StreamHandler(sys.stdout)
    std_out_handler.setLevel(logging.DEBUG)
    std_out_handler.setFormatter(formatter)
    std_out_handler.addFilter(InfoFilter())

    std_err_handler = logging.StreamHandler()
    std_err_handler.setLevel(logging.WARNING)
    std_err_handler.setFormatter(formatter)

    logger.addHandler(std_out_handler)
    logger.addHandler(std_err_handler)

    return logger