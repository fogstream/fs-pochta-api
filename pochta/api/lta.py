from typing import List

from pochta.utils import HTTPMethod


class LTA:
    def __init__(self, client) -> None:
        """
        Инициализация API Долгосрочного хранения.

        :param client: API клиент Доставки
        """
        self._client = client

    def search_shipments(self, query) -> List[dict]:
        """
        Запрос данных о партиях в архиве.

        https://otpravka.pochta.ru/specification#/long-term-archive-search_shipments

        :param query: Условие для поиска: номер заказа или ШПИ
        :return: Результат поиска в архиве
        """
        url = '/1.0/long-term-archive/shipment/search'

        params = {'query': query}

        res = self._client.request(HTTPMethod.GET, url, params=params)
        return res.json()
