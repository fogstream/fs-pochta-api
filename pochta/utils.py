from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict
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
    def raw(self) -> Dict:
        raise NotImplementedError()


def clean_data(data):
    if isinstance(data, list):
        data = [clean_data(each_data) for each_data in data]
    else:
        data = remap(data, lambda p, k, v: v is not None)

    return data
