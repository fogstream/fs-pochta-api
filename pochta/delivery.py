from base64 import b64encode

from requests import Request, Response, Session

from .api import (
    LTA,
    Archive,
    Batches,
    Documents,
    NoGroup,
    Orders,
    Services,
    Settings,
)
from .utils import clean_data


class Delivery:
    """
    API клиент сервиса Доставки.

    https://otpravka.pochta.ru/specification
    """

    API_URL = 'https://otpravka-api.pochta.ru'

    def __init__(self, login: str, password: str, access_token: str) -> None:
        """
        Инициализация API клиента Доставки.

        :param login: Логин от сервиса доставки
        :param password: Пароль от сервиса доставки
        :param access_token: Токен авторизации приложения
        """
        self._access_token = access_token
        self._auth_key = b64encode(f'{login}:{password}'.encode()).decode()
        self._session = Session()
        self._headers = {
            'Authorization': f'AccessToken {self._access_token}',
            'X-User-Authorization': f'Basic {self._auth_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=UTF-8',
        }
        self._session.headers.update(self._headers)

    def request(self, method: str, endpoint: str, data=None, **kwargs) -> Response:
        """
        Функция для обращения к API методам через протокол HTTP.

        :param method: HTTP метод
        :param endpoint: Эндпоинт API
        :param data: Тело запроса
        :param kwargs: Дополнительные аргументы
        :return: Ответ API
        """
        url = f'{self.API_URL}{endpoint}'
        stream = kwargs.pop('stream', False)
        if data:
            kwargs['json'] = clean_data(data)
        req = Request(method, url, **kwargs)
        prepared = self._session.prepare_request(req)
        res = self._session.send(prepared, stream=stream)
        res.raise_for_status()
        return res

    @property
    def archive(self) -> Archive:
        """Архив."""
        return Archive(self)

    @property
    def nogroup(self) -> NoGroup:
        """Данные."""
        return NoGroup(self)

    @property
    def lta(self) -> LTA:
        """Долгосрочное хранение."""
        return LTA(self)

    @property
    def services(self) -> Services:
        """Поиск ОПС."""
        return Services(self)

    @property
    def settings(self) -> Settings:
        """Настройки."""
        return Settings(self)

    @property
    def documents(self) -> Documents:
        """Документы."""
        return Documents(self)

    @property
    def batches(self) -> Batches:
        """Партии."""
        return Batches(self)

    @property
    def orders(self) -> Orders:
        """Заказы."""
        return Orders(self)
