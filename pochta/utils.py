from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Union
from uuid import uuid4

from boltons.iterutils import remap


class _AutoName(str, Enum):
    # pylint: disable=no-self-argument,unused-argument
    def _generate_next_value_(name, start, count, last_values):
        return name


class _UniqId(ABC):
    def __init__(self):
        self.id = str(uuid4())

    @property
    @abstractmethod
    def raw(self) -> dict:
        raise NotImplementedError()


def clean_data(data: Union[List, dict]) -> Union[List, dict]:
    """Метод рекурсивно очищающий словарь или список словарь от ключей со значением None."""
    if isinstance(data, list):
        data = [clean_data(each_data) for each_data in data]
    elif isinstance(data, dict):
        data = remap(data, lambda p, k, v: v is not None)
    else:
        data = data
    return data


class HTTPMethod(str, Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'
