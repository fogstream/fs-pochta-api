from typing import List

from pochta.utils import HTTPMethod


class Archive:
    def __init__(self, client) -> None:
        self._client = client

    def search_batches(self):
        """
        Запрос данных о партиях в архиве
        :return: Список партий в архивей
        """
        url = '/1.0/archive'
        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    def batch_to_archive(self, batch_names: List[str]):
        """
        Перевод партии в архив
        :param batch_names: Список с именами партий
        :return: Результат перевода
        """
        url = '/1.0/archive'
        res = self._client.request(HTTPMethod.PUT, url, data=batch_names)
        return res.json()

    def revert_batch(self, batch_names: List[str]):
        """
        Возврат партии из архива
        :param batch_names: Список с именами партий
        :return: Результат перевода
        """
        url = '/1.0/archive/revert'
        res = self._client.request(HTTPMethod.POST, url, data=batch_names)
        return res.json()
