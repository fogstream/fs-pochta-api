from typing import Dict, List, Optional

from pochta.utils import HTTPMethod


class Services:
    def __init__(self, client) -> None:
        self._client = client

    # TODO: Поиск ОПС по индексу
    # def postoffice(self, postal_code) -> Dict:
    #     url = f'/postoffice/1.0/{postal_code}'

    def postoffice_by_address(self, address: str, top: Optional[int] = 3):
        """
        Поиск обслуживающего ОПС по адресу
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

    def postoffice_service(self, postal_code: str):
        """
        Поиск почтовых сервисов ОПС
        Может возвращать как все доступные сервисы,
        так и сервисы определенной группы (например: Киберпочт@).
        :param postal_code: Индекс почтового отделения.
        :return: Почтовые сервисы в ОПС
        """
        url = f'/postoffice/1.0/{postal_code}/services'
        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    def postoffice_service_group(self, postal_code: str, group_id: str) -> List[Dict]:
        """
        Поиск почтовых сервисов ОПС по идентификатору группы сервисов
        Может возвращать как все доступные сервисы,
        так и сервисы определенной группы (например: Киберпочт@).
        :param postal_code: Индекс почтового отделения.
        :param group_id: Идентификатор группы сервисов.
        :return: Почтовые сервисы в ОПС
        """
        url = f'/postoffice/1.0/{postal_code}/services/{group_id}'
        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    # TODO: Поиск ОПС по координатам
    # def postoffice_nearby(self, lan: float, lon: float) -> List[Dict]:
    #     url = f'/postoffice/1.0/nearby'
    #     params = {
    #         'latitude': lan,
    #         'longitude': lon,
    #         'filter': ops_filter,
    #     }

    def postoffice_settlement_offices(self, settlement: str,
                                      region: Optional[str] = None,
                                      district: Optional[str] = None):
        """
        Поиск почтовых индексов в населённом пункте.
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
