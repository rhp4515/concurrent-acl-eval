import logging

def get_logger(name, path):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(path, mode='w')
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger