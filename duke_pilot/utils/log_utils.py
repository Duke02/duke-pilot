import functools
import logging
import sys
import typing as tp
from pathlib import Path

import numpy as np
import torch
from pydantic import BaseModel

from duke_pilot.utils.path_helper import get_logs_directory


class DukeLogger:
    def __init__(self, name: str, log_level: int = logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        p: Path = get_logs_directory() / f'{name}.log'
        p.parent.mkdir(parents=True, exist_ok=True)
        self.logger.addHandler(logging.FileHandler(str(p)))

    def _inner_serialize_arg(self, v: tp.Any) -> str:
        if isinstance(v, list):
            n: int = len(v)
            if n > 0:
                return f'[{self._serialize_arg(v[0])}, ...; n={n}]'
            return '[]'
        elif isinstance(v, dict):
            n: int = len(v)
            if n > 0:
                keys: list = list(v.keys())
                values: list = list(v.values())
                k: str = self._serialize_arg(keys[0])
                v: str = self._serialize_arg(values[0])
                return '{' + f'{k}={v}, ...; n={n}' + '}'
            return '{}'
        elif isinstance(v, BaseModel):
            return f'{type(v)}({self._serialize_arg(v.model_dump())})'
        elif isinstance(v, tuple):
            return f'({self._serialize_arg(v[0])}, ...; n={len(v)})'
        elif isinstance(v, np.ndarray):
            shape: tuple = v.shape
            dtype = v.dtype
            return f'NDArray(shape={shape}, dtype={dtype})'
        elif isinstance(v, torch.Tensor):
            shape: tuple = v.shape
            dtype = v.dtype
            return f'Tensor(shape={shape}, dtype={dtype})'
        elif isinstance(v, tp.BinaryIO):
            return f'BinaryFile'
        else:
            return str(v)

    def _serialize_arg(self, v: tp.Any, max_len: int = 20) -> str:
        out: str = self._inner_serialize_arg(v)
        if len(out) > max_len:
            return f'{out[:max_len]}...'
        else:
            return out

    def _log(self, level: int, msg: str, *args, **kwargs):
        args: list[str] = [self._serialize_arg(a) for a in args]
        kwargs: list[str] = [f'{self._serialize_arg(k)}={self._serialize_arg(v)}' for k, v in kwargs.items()]
        message: str = f'{msg} (args {args}, kwargs {kwargs})'
        self.logger.log(level, message)

    def info(self, msg: str, *args, **kwargs):
        self._log(logging.INFO, msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self._log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self._log(logging.ERROR, msg, *args, **kwargs)

    def log(self, func: tp.Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.debug(f'Calling function {func.__name__}', *args, **kwargs)
            try:
                result = func(*args, **kwargs)
                self.debug(f'{func.__name__} got result of {self._serialize_arg(result)}')
                return result
            except Exception as e:
                self.error(f"Exception raised in {func.__name__}. exception: {str(e)}")
                raise e
        return wrapper

    async def alog(self, func: tp.Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            self.debug(f'Calling function {func.__name__}', *args, **kwargs)
            try:
                result = await func(*args, **kwargs)
                self.debug(f'{func.__name__} got result of {self._serialize_arg(result)}')
                return result
            except Exception as e:
                self.error(f"Exception raised in {func.__name__}. exception: {str(e)}")
                raise e
        return wrapper
