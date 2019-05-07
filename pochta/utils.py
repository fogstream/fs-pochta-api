from enum import Enum
from uuid import uuid4

from boltons.iterutils import remap


class _AutoName(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class _UniqId:
    def __init__(self):
        self.id = str(uuid4())


def clean_data(data):
    if isinstance(data, list):
        data = [clean_data(each_data) for each_data in data]
    else:
        data = remap(data, lambda p, k, v: v is not None)

    return data
