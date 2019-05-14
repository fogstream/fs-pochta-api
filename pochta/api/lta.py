from __future__ import annotations

from typing import TYPE_CHECKING, List

from pochta.utils import HTTPMethod


if TYPE_CHECKING:
    from pochta import Delivery


class LTA:
    """
    Методы API Долгосрочного хранения.

    Используется через объект :class:`Delivery <pochta.delivery.Delivery>` или вручную.
    """

    def __init__(self, client: Delivery) -> None:
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
