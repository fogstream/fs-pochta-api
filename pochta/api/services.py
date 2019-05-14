from __future__ import annotations

from datetime import datetime
import json
from typing import TYPE_CHECKING, List, Optional, Union

from pochta.enums import PostofficeWorkType
from pochta.utils import HTTPMethod


if TYPE_CHECKING:
    from pochta import Delivery


class Services:
    """
    Методы API Поиска ОПС.

    Используется через объект :class:`Delivery <pochta.delivery.Delivery>` или вручную.
    """

    def __init__(self, client: Delivery) -> None:
        """
        Инициализация API Поиска ОПС.

        :param client: API клиент Доставки
        """
        self._client = client

    def get_postoffice(self, postal_code: Union[str, int]) -> dict:
        """
        Поиск почтового отделения по индексу.

        https://otpravka.pochta.ru/specification#/services-postoffice

        :param postal_code: Индекс почтового отделения
        :return: Результат операции
        """
        url = f'/postoffice/1.0/{postal_code}'

        params = {'ufps-postal-code': True}

        res = self._client.request(HTTPMethod.GET, url, params=params)
        return res.json()

    def get_postoffice_by_address(self, address: str, top: Optional[int] = 3):
        """
        Поиск обслуживающего ОПС по адресу.

        https://otpravka.pochta.ru/specification#/services-postoffice-by-address

        :param address: Строка с адресом. Следует учесть, что чем точнее адрес,
            тем точнее будет поиск. Пример: Санкт-Петербург, улица Победы, 15к1
        :param top: Количество ближайших почтовых отделений в результате поиска (Опционально).
            По умолчанию равно 3.
        :return: Список почтовых индексов найденных ОПС отсортированный по релевантности
        """
        url = '/postoffice/1.0/by-address'

        params = {
            'address': address,
            'top': top,
        }

        res = self._client.request(HTTPMethod.GET, url, params=params)
        return res.json()

    def get_postoffice_services(self, postal_code: Union[str, int]) -> List[dict]:
        """
        Поиск почтовых сервисов ОПС.

        Может возвращать как все доступные сервисы,
        так и сервисы определенной группы (например: Киберпочт@).

        https://otpravka.pochta.ru/specification#/services-postoffice-service

        :param postal_code: Индекс почтового отделения.
        :return: Почтовые сервисы в ОПС
        """
        url = f'/postoffice/1.0/{postal_code}/services'

        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    def get_postoffice_service_group(self, postal_code: Union[str, int],
                                     group_id: str) -> List[dict]:
        """
        Поиск почтовых сервисов ОПС по идентификатору группы сервисов.

        https://otpravka.pochta.ru/specification#/services-postoffice-service-group

        :param postal_code: Индекс почтового отделения.
        :param group_id: Идентификатор группы сервисов.
        :return: Почтовые сервисы в ОПС
        """
        url = f'/postoffice/1.0/{postal_code}/services/{group_id}'

        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    def get_nearby_postoffices(self, lan: float, lon: float,
                               top: Optional[int] = None,
                               work_filter: PostofficeWorkType = PostofficeWorkType.ALL,
                               search_radius: Optional[float] = None,
                               current_date_time: Optional[datetime] = None,
                               hide_private: Optional[bool] = False,
                               filter_by_office_type: Optional[bool] = True,
                               yandex_address: Optional[str] = None,
                               geo_object: Optional[str] = None) -> List[dict]:
        """
        Поиск почтовых отделений по координатам.

        https://otpravka.pochta.ru/specification#/services-postoffice-nearby

        :param lan: Широта
        :param lon: Долгота
        :param top: Количество ближайших почтовых отделений в результате поиска
        :param work_filter: Дополнительное ограничение по времени работы для поиска ОПС.
        :param search_radius: Радиус для поиска (в километрах)
        :param current_date_time: Текущее клиентское дата-время в таймзоне клиента.
            Формат: yyyy-MM-dd'T'HH:mm:ss. Данный параметр используется для определения отделений,
            работающих в данный момент, т.е. если эти данные нужны, параметр передавать обязательно!
        :param hide_private: Исключать не публичные отделения. По-умолчанию не исключать (false).
        :param filter_by_office_type: Фильтр по типам объектов в ответе.
            true: ГОПС, СОПС, ПОЧТОМАТ. false: все. Значение по-умолчанию - true.
        :param yandex_address: Адрес в том формате, в котором возвращает его сервис Яндекса для
            адреса, указанного пользователем. Пример: Санкт-Петербург, улица Победы, 15к1.
            Параметр необходим для определения является ли переданный адрес точным адресом
            отделения. Требует также заполненного параметра geoObject.
        :param geo_object: JSON-строка, содержащая объект GeoObject, получаемый для адреса в
            сервисе Яндекса. См. api.yandex.ru.
            Требует также заполненного параметра 'yandex-address'.
        :return: Результат операции
        """
        url = f'/postoffice/1.0/nearby'

        if isinstance(current_date_time, datetime):
            current_date_time = current_date_time.isoformat()

        if yandex_address and not geo_object:
            raise AttributeError('Требуется указать geo_object')
        if geo_object and not yandex_address:
            raise AttributeError('Требуется указать yandex_address')
        if geo_object and yandex_address:
            try:
                json.loads(geo_object)
            except ValueError:
                raise AttributeError('Параметр geo_object должен быть валидным json объектом')

        params = {
            'latitude': lan,
            'longitude': lon,
            'top': top,
            'filter': work_filter,
            'search-radius': search_radius,
            'current-date-time': current_date_time,
            'hide-private': hide_private,
            'filter-by-office-type': filter_by_office_type,
            'yandex-address': yandex_address,
            'geo-object': geo_object,
        }

        res = self._client.request(HTTPMethod.GET, url, params=params)
        return res.json()

    def get_settlement_postoffices(self, settlement: str,
                                   region: Optional[str] = None,
                                   district: Optional[str] = None) -> List[str]:
        """
        Поиск почтовых индексов в населённом пункте.

        https://otpravka.pochta.ru/specification#/services-postoffice-settlement.offices.codes

        :param region: Область/край/республика, где расположен населённый пункт
            (например Свердловская).
        :param district: Район, где расположен населённый пункт
            (для деревень, посёлков и т. д. - например Сухоложский).
        :param settlement: Название населённого пункта (например Екатеринбург)
        :return: Список почтовых индексов.
        """
        url = '/postoffice/1.0/settlement.offices.codes'

        params = {
            'settlement': settlement,
            'region': region,
            'district': district,
        }

        res = self._client.request(HTTPMethod.GET, url, params=params)
        return res.json()
