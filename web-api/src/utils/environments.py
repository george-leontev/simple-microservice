import os

class EnvironmentHelper:

    @staticmethod
    def is_production():
        env = os.environ.get('ENVIRONMENT')
        return env is not None and env == 'production'


