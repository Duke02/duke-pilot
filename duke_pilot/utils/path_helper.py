from pathlib import Path


def get_base_directory() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def get_data_directory() -> Path:
    return get_base_directory() / 'data'


def get_model_directory() -> Path:
    return get_base_directory() / 'models'


def get_logs_directory() -> Path:
    return get_base_directory() / 'logs'
