import os
from dotenv import load_dotenv


def load() -> None:
    load_dotenv(dotenv_path=os.path.dirname(os.path.abspath(__file__)) + "/../../../.env")
