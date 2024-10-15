from src.main.bootstrap.bootstrap import load

from src.main.configs.app import application


def init():
    load()
    return application()
