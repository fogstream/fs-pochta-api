from __future__ import annotations

from typing import TYPE_CHECKING, List

from pochta.helpers import Order
from pochta.utils import HTTPMethod


if TYPE_CHECKING:
    from pochta import Delivery


class Orders:
    """
    Методы API Заказов.

    Используется через объект :class:`Delivery <pochta.delivery.Delivery>` или вручную.
    """

    def __init__(self, client: Delivery) -> None:
        """
        Инициализация API Заказов.

        :param client: API клиент Доставки
        """
        self._client = client

    def create_order(self, orders: List[Order]) -> dict:
        """
        Создание заказа.

        Создает новый заказ. Автоматически рассчитывает и проставляет плату за пересылку.

        https://otpravka.pochta.ru/specification#/orders-creating_order

        :param orders: Список заказов
        :return: Результат операции
        """
        url = '/1.0/user/backlog'

        orders = [order.raw for order in orders]

        res = self._client.request(HTTPMethod.PUT, url, data=orders)
        return res.json()

    def edit_order(self, shipment_id: str, order: Order) -> dict:
        """
        Редактирование заказа.

        https://otpravka.pochta.ru/specification#/orders-editing_order

        :param shipment_id: Внутренний идентификатор отправления
        :param order: Измененный заказ
        :return: Результат операции
        """
        url = f'/1.0/backlog/{shipment_id}'

        res = self._client.request(HTTPMethod.PUT, url, data=order.raw)
        return res.json()

    def search_order(self, query: str) -> List[dict]:
        """
        Поиск заказа.

        Ищет заказы по назначенному магазином идентификатору.

        https://otpravka.pochta.ru/specification#/orders-search_order

        :param query: Буквенно-цифровой идентификатор отправления
        :return: Результат операции
        """
        url = '/1.0/backlog/search'

        params = {'query': query}

        res = self._client.request(HTTPMethod.GET, url, params=params)
        return res.json()

    def search_order_by_id(self, order_id: str) -> dict:
        """
        Поиск заказа по идентификатору.

        https://otpravka.pochta.ru/specification#/orders-search_order_byid

        :param order_id: Внутренний идентификатор отправления
        :return: Результат операции
        """
        url = f'/1.0/backlog/{order_id}'

        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    def delete_order(self, backlog_ids: List[str]) -> dict:
        """
        Удаление заказа.

        https://otpravka.pochta.ru/specification#/orders-delete_new_order

        :param backlog_ids: Список уникальных идентификаторов заказов
        :return: Результат операции
        """
        url = '/1.0/backlog'

        res = self._client.request(HTTPMethod.DELETE, url, data=backlog_ids)
        return res.json()

    def shipment_to_backlog(self, shipment_ids: List[str]) -> dict:
        """
        Возврат заказов в "Новые".

        Метод переводит заказы из партии в раздел Новые. Партия должна быть в статусе CREATED.

        https://otpravka.pochta.ru/specification#/orders-shipment_to_backlog

        :param shipment_ids: Список внутренних идентификаторов заказов
        :return: Результат операции
        """
        url = '/1.0/user/backlog'

        res = self._client.request(HTTPMethod.POST, url, data=shipment_ids)
        return res.json()
