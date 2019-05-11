from typing import Dict, List

from pochta.utils import HTTPMethod


class LTA:
    def __init__(self, client) -> None:
        self._client = client

    def search_shipments(self, query) -> List[Dict]:
        """
        Запрос данных о партиях в архиве
        :param query: Условие для поиска: номер заказа или ШПИ
        :return: Результат поиска в архиве
        """
        url = '/1.0/long-term-archive/shipment/search'
        params = {'query': query}
        res = self._client.request(HTTPMethod.GET, url, params=params)
        return res.json()
