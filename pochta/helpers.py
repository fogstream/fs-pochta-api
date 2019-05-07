from typing import Optional

from utils import _UniqId


class Address(_UniqId):
    def __init__(self, address: str):
        """
        Адрес для нормализации
        :param address: Оригинальный адрес одной строкой
        """
        super().__init__()
        self.address = address

    def __str__(self):
        return self.address


class Name(_UniqId):
    def __init__(self, name: str):
        """
        ФИО для нормализации
        :param name: Оригинальные фамилия, имя , отчество одной строкой
        """
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        return self.name


class Phone(_UniqId):
    def __init__(self, phone: str,
                 area: Optional[str] = None,
                 place: Optional[str] = None,
                 region: Optional[str] = None):
        """
        Телефон для нормализации
        :param phone: Оригинальный номер одной строкой
        :param area: Область/край трелефонного номера
        :param place: Город телефонного номера
        :param region: Регион телефонного номера
        """
        super().__init__()
        self.phone = phone
        self.area = area
        self.place = place
        self.region = region

    def __str__(self) -> str:
        return self.phone
