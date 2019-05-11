from base64 import b64encode

from requests import Request, Response, Session

from pochta.api import (
    LTA,
    Archive,
    Batches,
    Documents,
    NoGroup,
    Orders,
    Services,
    Settings,
)
from pochta.utils import clean_data


class Delivery:
    API_URL = 'https://otpravka-api.pochta.ru'

    def __init__(self, login: str, password: str, access_token: str) -> None:
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
        return Archive(self)

    @property
    def nogroup(self) -> NoGroup:
        return NoGroup(self)

    @property
    def lta(self) -> LTA:
        return LTA(self)

    @property
    def services(self) -> Services:
        return Services(self)

    @property
    def settings(self) -> Settings:
        return Settings(self)

    @property
    def documents(self) -> Documents:
        return Documents(self)

    @property
    def batches(self) -> Batches:
        return Batches(self)

    @property
    def orders(self) -> Orders:
        return Orders(self)
