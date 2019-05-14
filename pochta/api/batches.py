from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, List, Optional

from pochta.enums import MailCategory, MailType
from pochta.helpers import Order
from pochta.utils import HTTPMethod


if TYPE_CHECKING:
    from pochta import Delivery


class Batches:
    """
    Методы API Партий.

    Используется через объект :class:`Delivery <pochta.delivery.Delivery>` или вручную.
    """

    def __init__(self, client: Delivery) -> None:
        """
        Инициализация API Партий.

        :param client: API клиент Доставки
        """
        self._client = client

    def create_batch(self, shipment_ids: List[str], sending_date: Optional[date] = None) -> dict:
        """
        Создание партии из N заказов.

        Автоматически создает партию и переносит указанные подготовленные заказы в эту партию.
        Если заказы относятся к разным типам и категориям – создается несколько партий.
        Заказы распределяются по соответствующим партиям.
        Каждому перенесенному заказу автоматически присваивается ШПИ.

        https://otpravka.pochta.ru/specification#/batches-create_batch_from_N_orders

        :param shipment_ids: Список внутренних идентификаторов заказов
        :param sending_date: Дата сдачи в почтовое отделение (yyyy-MM-dd)
        :return: Результат операции
        """
        url = '/1.0/user/shipment'

        if isinstance(sending_date, date):
            sending_date = sending_date.isoformat()

        params = {'sending-date': sending_date}

        res = self._client.request(HTTPMethod.POST, url, data=shipment_ids, params=params)
        return res.json()

    def change_sending_date(self, batch_name: int, year: int, month: int, day: int) -> dict:
        """
        Изменение дня отправки в почтовое отделение.

        Изменяет (устанавливает) новый день отправки в почтовое отделение.

        https://otpravka.pochta.ru/specification#/batches-sending_date

        :param batch_name: Наименование партии
        :param year: Дата сдачи в почтовое отделение: год
        :param month: Дата сдачи в почтовое отделение: месяц
        :param day: Дата сдачи в почтовое отделение: день
        :return: Результат операции
        """
        url = f'/1.0/batch/{batch_name}/sending/{year}/{month}/{day}'

        res = self._client.request(HTTPMethod.POST, url)
        return res.json()

    def move_orders_to_batch(self, batch_name: str, shipment_ids: List[str]) -> dict:
        """
        Перенос заказов в партию.

        Переносит подготовленные заказы в указанную партию.
        Если часть заказов не может быть помещена в партию (тип и категория партии
        не соответствует типу и категории заказа) - возвращается json объект с указанием индекса
        заказа в переданном массиве и типом ошибки, остальные заказы помещаются в указанную партию.
        Каждому перенесенному заказу автоматически присваивается ШПИ.

        https://otpravka.pochta.ru/specification#/batches-move_orders_to_batch

        :param batch_name: Наименование партии
        :param shipment_ids: Список внутренних идентификаторов заказов
        :return: Результат операции
        """
        url = f'/1.0/batch/{batch_name}/shipment'

        res = self._client.request(HTTPMethod.POST, url, data=shipment_ids)
        return res.json()

    def find_batch(self, batch_name: str) -> dict:
        """
        Поиск партии по наименованию.

        Возвращает параметры партии.
        https://otpravka.pochta.ru/specification#/batches-find_batch

        :param batch_name: Наименование партии
        :return: Результат операции
        """
        url = f'/1.0/batch/{batch_name}'

        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    def find_orders_with_barcode(self, query: str) -> List[dict]:
        """
        Поиск заказов с ШПИ.

        https://otpravka.pochta.ru/specification#/batches-find_orders_with_barcode

        :param query: Условие для поиска: номер заказа или ШПИ
        :return: Результат операции
        """
        url = '/1.0/shipment/search'

        params = {'query': query}

        res = self._client.request(HTTPMethod.GET, url, params=params)
        return res.json()

    def add_orders_to_batch(self, batch_name: str, orders: List[Order]) -> dict:
        """
        Добавление заказов в партию.

        Создает массив заказов и помещает непосредственно в партию. Автоматически рассчитывает
        и проставляет плату за пересылку. Каждому заказу автоматически присваивается ШПИ.

        https://otpravka.pochta.ru/specification#/batches-add_orders_to_batch

        :param batch_name: Наименование партии
        :param orders: Список заказов
        :return: Результат операции
        """
        url = f'/1.0/batch/{batch_name}/shipment'

        orders = [order.raw for order in orders]

        res = self._client.request(HTTPMethod.GET, url, data=orders)
        return res.json()

    def delete_order_from_batch(self, shipment_ids: List[str]) -> dict:
        """
        Удаление заказов из партии.

        https://otpravka.pochta.ru/specification#/batches-delete_order_from_batch

        :param shipment_ids: Список внутренних идентификаторов заказов
        :return: Результат операции
        """
        url = '/1.0/shipment'

        res = self._client.request(HTTPMethod.GET, url, data=shipment_ids)
        return res.json()

    def get_batch_orders_info(self, batch_name: str,
                              sort: str = 'asc',
                              size: Optional[int] = None,
                              page: Optional[int] = None) -> List[dict]:
        """
        Запрос данных о заказах в партии.

        https://otpravka.pochta.ru/specification#/batches-get_info_about_orders_in_batch

        :param batch_name: Наименование партии
        :param sort: Критерии сортировки в формате: asc(по возрастанию) или desc (по убыванию).
            По умолчанию порядок сортировки по возрастанию
        :param size: Количество записей на странице
        :param page: Номер страницы (0..N)
        :return: Результат операции
        """
        url = f'/1.0/batch/{batch_name}/shipment'

        params = {
            'sort': sort,
            'size': size,
            'page': page,
        }

        res = self._client.request(HTTPMethod.GET, url, params=params)
        return res.json()

    def search_all_batches(self, mail_type: Optional[MailType] = None,
                           mail_category: Optional[MailCategory] = None,
                           sort: Optional[str] = 'asc',
                           size: Optional[int] = None,
                           page: Optional[int] = None) -> List[dict]:
        """
        Поиск всех партий.

        https://otpravka.pochta.ru/specification#/batches-search_all_batches

        :param mail_type: Тип отправления (По умолчанию: ВСЕ)
        :param mail_category: Категория отправления (По умолчанию: ВСЕ)
        :param sort: Критерии сортировки в формате: asc(по возрастанию) или desc (по убыванию).
            По умолчанию порядок сортировки по возрастанию
        :param size: Количество записей на странице
        :param page: Номер страницы (0..N)
        :return: Результат операции
        """
        url = '/1.0/batch'

        params = {
            'mailType': mail_type,
            'mailCategory': mail_category,
            'sort': sort,
            'size': size,
            'page': page,
        }

        res = self._client.request(HTTPMethod.GET, url, params=params)
        return res.json()

    def find_order_by_id(self, shipment_id: str) -> dict:
        """
        Поиск заказа в партии по внутреннему id.

        https://otpravka.pochta.ru/specification#/batches-find_order_by_id

        :param shipment_id: Внутренний идентификатор отправления
        :return: Результат операции
        """
        url = f'/1.0/shipment/{shipment_id}'

        res = self._client.request(HTTPMethod.GET, url)
        return res.json()
