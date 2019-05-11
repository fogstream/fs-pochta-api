from typing import List

from pochta.utils import HTTPMethod


class Orders:
    def __init__(self, client) -> None:
        self._client = client

    # # TODO: Создание заказа
    # def create_order(self):
    #     ...
    #
    # # TODO: Редактирование заказа
    # def edit_order(self):
    #     ...
    #
    def search_order(self, query: str):
        url = '/1.0/backlog/search'
        params = {'query': query}
        res = self._client.request(HTTPMethod.GET, url, params=params)
        return res.json()

    def search_order_by_id(self, order_id: str):
        url = f'/1.0/backlog/{order_id}'
        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    def delete_new_order(self, orders: List[str]):
        url = '/1.0/backlog'
        res = self._client.request(HTTPMethod.DELETE, url, data=orders)
        return res.json()

    def shipment_to_backlog(self, orders: List[str]):
        url = '/1.0/user/backlog'
        res = self._client.request(HTTPMethod.POST, url, data=orders)
        return res.json()
