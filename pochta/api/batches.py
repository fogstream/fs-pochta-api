from datetime import date
from typing import Dict, List, Optional

from pochta.enums import MailCategory, MailType
from pochta.utils import HTTPMethod


class Batches:
    def __init__(self, client) -> None:
        self._client = client

    def create_batch(self, shipment_ids: List[str], sending_date: Optional[date] = None) -> Dict:
        url = '/1.0/user/shipment'
        if isinstance(sending_date, date):
            sending_date = sending_date.isoformat()
        params = {'sending-date': sending_date}
        res = self._client.request(HTTPMethod.POST, url, data=shipment_ids, params=params)
        return res.json()

    def sending_date(self, batch_name: int, year: int, month: int, day: int) -> Dict:
        url = f'/1.0/batch/{batch_name}/sending/{year}/{month}/{day}'
        res = self._client.request(HTTPMethod.POST, url)
        return res.json()

    def move_orders_to_batch(self, batch_name: str, shipment_ids: List[str]) -> Dict:
        url = f'/1.0/batch/{batch_name}/shipment'
        res = self._client.request(HTTPMethod.POST, url, data=shipment_ids)
        return res.json()

    def find_batch(self, batch_name: str) -> Dict:
        url = f'/1.0/batch/{batch_name}'
        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    def find_orders_with_barcode(self, query: str) -> List[Dict]:
        url = '/1.0/shipment/search'
        params = {'query': query}
        res = self._client.request(HTTPMethod.GET, url, params=params)
        return res.json()

    # TODO: Сделать после создания заказа
    # def add_orders_to_batch(self, batch_name: str):
    #     url = f'/1.0/batch/{batch_name}/shipment'

    def delete_order_from_batch(self, shipment_ids: List[str]) -> Dict:
        url = '/1.0/shipment'
        res = self._client.request(HTTPMethod.GET, url, data=shipment_ids)
        return res.json()

    def get_info_about_orders_in_batch(self, batch_name: str,
                                       sort: str = 'asc',
                                       size: Optional[int] = None,
                                       page: Optional[int] = None) -> List[Dict]:
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
                           page: Optional[int] = None) -> List[Dict]:
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

    def find_order_by_id(self, shipment_id: str) -> Dict:
        url = f'/1.0/shipment/{shipment_id}'
        res = self._client.request(HTTPMethod.GET, url)
        return res.json()
