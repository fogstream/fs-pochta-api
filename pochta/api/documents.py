from datetime import date
from typing import Dict, Optional

from requests import Response

from pochta.enums import PrintType
from pochta.utils import HTTPMethod


class Documents:
    def __init__(self, client) -> None:
        self._client = client

    def create_all_docs(self, batch_name: str) -> Response:
        url = f'/1.0/forms/{batch_name}/zip-all'
        res = self._client.request(HTTPMethod.GET, url, stream=True)
        return res

    def create_f7_f22(self, order_id: str, sending_date: Optional[date] = None,
                      print_type: Optional[PrintType] = None) -> Response:
        url = f'/1.0/forms/{order_id}/f7pdf'
        if isinstance(sending_date, date):
            sending_date = sending_date.isoformat()
        params = {
            'sending-date': sending_date,
            'print-type': print_type,
        }
        res = self._client.request(HTTPMethod.GET, url, params=params, stream=True)
        return res

    def create_f112(self, order_id: str, sending_date: Optional[date] = None) -> Response:
        url = f'/1.0/forms/{order_id}/f112pdf'
        if isinstance(sending_date, date):
            sending_date = sending_date.isoformat()
        params = {'sending-date': sending_date}
        res = self._client.request(HTTPMethod.GET, url, params=params, stream=True)
        return res

    def create_forms_backlog(self, order_id: str, sending_date: Optional[date] = None) -> Response:
        url = f'/1.0/forms/backlog/{order_id}/forms'
        if isinstance(sending_date, date):
            sending_date = sending_date.isoformat()
        params = {'sending-date': sending_date}
        res = self._client.request(HTTPMethod.GET, url, params=params, stream=True)
        return res

    def create_forms(self, order_id: str, sending_date: Optional[date] = None,
                     print_type: Optional[PrintType] = None) -> Response:
        url = f'/1.0/forms/{order_id}/forms'
        if isinstance(sending_date, date):
            sending_date = sending_date.isoformat()
        params = {
            'sending-date': sending_date,
            'print-type': print_type,
        }
        res = self._client.request(HTTPMethod.GET, url, params=params, stream=True)
        return res

    def create_f103(self, batch_name: str) -> Response:
        url = f'/1.0/forms/{batch_name}/f103pdf'
        res = self._client.request(HTTPMethod.GET, url, stream=True)
        return res

    def checkin(self, batch_name: str) -> Dict:
        url = f'/1.0/batch/{batch_name}/checkin'
        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    def create_comp_check_form(self, batch_name: str) -> Response:
        url = f'/1.0/forms/{batch_name}/completeness-checking-form'
        res = self._client.request(HTTPMethod.GET, url, stream=True)
        return res
