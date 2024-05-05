import os


def is_production():
    return os.environ.get('PRODUCTION') is not None