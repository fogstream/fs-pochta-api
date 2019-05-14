from __future__ import annotations

from typing import TYPE_CHECKING, List

from pochta.utils import HTTPMethod


if TYPE_CHECKING:
    from pochta import Delivery


class Archive:
    """
    Методы API Архива.

    Используется через объект :class:`Delivery <pochta.delivery.Delivery>` или вручную.
    """

    def __init__(self, client: Delivery) -> None:
        """
        Инициализация API Архива.

        :param client: API клиент Доставки
        """
        self._client = client

    def get_archive_batches(self) -> List[dict]:
        """
        Запрос данных о партиях в архиве.

        https://otpravka.pochta.ru/specification#/archive-search_batches

        :return: Список партий в архиве
        """
        url = '/1.0/archive'

        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    def batch_to_archive(self, batch_names: List[str]) -> List[dict]:
        """
        Перевод партии в архив.

        https://otpravka.pochta.ru/specification#/archive-batch_to_archive

        :param batch_names: Список с именами партий
        :return: Результат перевода
        """
        url = '/1.0/archive'

        res = self._client.request(HTTPMethod.PUT, url, data=batch_names)
        return res.json()

    def revert_batch(self, batch_names: List[str]) -> List[dict]:
        """
        Возврат партии из архива.

        https://otpravka.pochta.ru/specification#/archive-revert_batch

        :param batch_names: Список с именами партий
        :return: Результат перевода
        """
        url = '/1.0/archive/revert'

        res = self._client.request(HTTPMethod.POST, url, data=batch_names)
        return res.json()
