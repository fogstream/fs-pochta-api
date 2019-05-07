from typing import Dict, Optional

from .utils import _UniqId


class Address(_UniqId):
    def __init__(self, address: str):
        """
        Адрес для нормализации
        :param address: Оригинальный адрес одной строкой
        """
        super().__init__()
        self.address = address

    @property
    def raw(self) -> Dict:
        return {'id': self.id, 'original-address': self.address}

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

    @property
    def raw(self) -> Dict:
        return {'id': self.id, 'original-fio': self.name}

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

    @property
    def raw(self) -> Dict:
        return {
            'id': self.id,
            'original-phone': self.phone,
            'area': self.area,
            'place': self.place,
            'region': self.region,
        }

    def __str__(self) -> str:
        return self.phone


class Recipient(_UniqId):
    def __init__(self, address: str, full_name: str, phone: str):
        """
        Получатель для проверки благонадежности
        :param address: Адрес
        :param full_name: Полное имя
        :param phone: Телефон
        """
        super().__init__()
        self.address = address
        self.full_name = full_name
        self.phone = phone

    @property
    def raw(self) -> Dict:
        return {
            'raw-address': self.address,
            'raw-full-name': self.full_name,
            'raw-telephone': self.phone,
        }

    def __str__(self):
        return self.full_name
