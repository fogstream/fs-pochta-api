from base64 import b64encode
import json
from typing import Dict, List, Optional

from requests import Request, Session

from .enums import EntryType, MailCategory, MailType, PaymentType, TransportType
from .helpers import Address, Name, Phone, Recipient
from .utils import clean_data


class Delivery:
    API_URL = 'https://otpravka-api.pochta.ru'

    def __init__(self, login: str, password: str, access_token: str):
        self._access_token = access_token
        self._auth_key = b64encode(f'{login}:{password}'.encode()).decode()
        self._session = Session()
        self._headers = {
            'Authorization': f'AccessToken {self._access_token}',
            'X-User-Authorization': f'Basic {self._auth_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=UTF-8',
        }
        self._session.headers.update(self._headers)

    def _request(self, method: str, endpoint: str, data=None, **kwargs):
        url = f'{self.API_URL}{endpoint}'
        if data:
            data = clean_data(data)
            data = json.dumps(data).encode()
        req = Request(method, url, data=data, **kwargs)
        prepared = self._session.prepare_request(req)
        res = self._session.send(prepared)
        res.raise_for_status()
        return res

    # region Данные
    def clean_address(self, addresses: List[Address]) -> Dict:
        """
        Разделяет и помещает сущности переданных адресов (город, улица)
        в соответствующие поля возвращаемого объекта.
        Параметр id (идентификатор записи) используется для установления
        соответствия переданных и полученных записей, так как порядок
        сортировки возвращаемых записей не гарантируется.
        Метод автоматически ищет и возвращает индекс близлежащего
        ОПС по указанному адресу.
        :param addresses:  Список адрессов
        :return: Результат нормализации
        """
        url = f'/1.0/clean/address'
        data = [address.raw for address in addresses]
        res = self._request('post', url, data=data)
        return res.json()

    def clean_physical(self, names: List[Name]) -> Dict:
        """
        Очищает, разделяет и помещает значения ФИО в соответствующие
        поля возвращаемого объекта. Параметр id (идентификатор записи)
        используется для установления соответствия переданных и полученных
        записей, так как порядок сортировки возвращаемых
        записей не гарантируется.
        :param names: Список имен
        :return: Результат нормализации
        """
        url = f'/1.0/clean/physical'
        data = [name.raw for name in names]
        res = self._request('post', url, data=data)
        return res.json()

    def clean_phone(self, phone_numbers: List[Phone]) -> Dict:
        """
        Принимает номера телефонов в неотформатированном виде, который может
        включать пробелы, символы: +-(). Очищает, разделяет и помещает сущности
        телефона (код города, номер) в соответствующие поля возвращаемого
        объекта. Если номер телефона 11-ти значный (мобильный),
        то дополнительные параметры, кроме original-phone и id,
        указывать не обязательно. Если номер телефона стационарный,
        то необходимо опционально указать дополнительные параметры для
        определения кода города. Параметр id (идентификатор записи)
        используется для установления соответствия переданных и полученных
        записей, так как порядок сортировки возвращаемых
        записей не гарантируется.
        :param phone_numbers: Список номеров
        :return: Результат нормализации
        """
        url = '/1.0/clean/phone'
        data = [phone.raw for phone in phone_numbers]
        res = self._request('post', url, data=data)
        return res.json()

    def check_unreliable_recipient(self, recipients: List[Recipient]):
        url = '/1.0/unreliable-recipient'
        data = [recipient.raw for recipient in recipients]
        res = self._request('post', url, data=data)
        return res.json()

    @property
    def balance(self) -> Dict:
        """
        Отображает баланс расчетного счета.
        Возвращаемые значения указываются в копейках.
        :return: Баланс
        """
        url = '/1.0/counterpart/balance'
        res = self._request('get', url)
        return res.json()

    def calc_delivery(self, completeness_checking: Optional[bool] = None,
                      courier: Optional[bool] = None,
                      declared_value: Optional[int] = None,
                      height: Optional[int] = None,
                      length: Optional[int] = None,
                      width: Optional[int] = None,
                      entries_type: Optional[EntryType] = None,
                      fragile: Optional[bool] = None,
                      index_from: Optional[str] = None,
                      index_to: Optional[str] = None,
                      mail_category: MailCategory = MailCategory.SIMPLE,
                      mail_direct: Optional[int] = None,
                      mail_type: MailType = MailType.POSTAL_PARCEL,
                      mass: int = 100,
                      notice_payment_method: Optional[PaymentType] = None,
                      payment_method: Optional[PaymentType] = None,
                      sms_notice_recipient: Optional[int] = None,
                      transport_type: Optional[TransportType] = None,
                      with_order_of_notice: bool = False,
                      with_simple_notice: bool = False) -> Dict:
        """
        Рассчитывает стоимость пересылки в зависимости от указанных
        входных данных. Индекс ОПС точки отправления берется из профиля
        клиента. Возвращаемые значения указываются в копейках.
        :param completeness_checking: Признак услуги проверки комплектности
        :param courier: Отметка "Курьер"
        :param declared_value: Объявленная ценность
        :param height: Линейная высота (сантиметры)
        :param length: Линейная длина (сантиметры)
        :param width: Линейная ширина (сантиметры)
        :param entries_type: Категория вложения.
        https://otpravka.pochta.ru/specification#/enums-base-entries-type
        :param fragile: Отметка "Осторожно/Хрупко"
        :param index_from: Почтовый индекс объекта почтовой связи места приема
        :param index_to: Почтовый индекс объекта почтовой связи места назначения
        :param mail_category: Категория РПО
        https://otpravka.pochta.ru/specification#/enums-base-mail-category
        :param mail_direct: Код страны назначения.
        https://otpravka.pochta.ru/specification#/dictionary-countries
        :param mail_type: Вид РПО
        https://otpravka.pochta.ru/specification#/enums-base-mail-type
        :param mass: Масса отправления в граммах
        :param notice_payment_method: Способ оплаты уведомеления.
        https://otpravka.pochta.ru/specification#/enums-payment-methods
        :param payment_method: Способ оплаты.
        https://otpravka.pochta.ru/specification#/enums-payment-methods
        :param sms_notice_recipient: Признак услуги SMS уведомления
        :param transport_type: Вид транспортировки
        https://otpravka.pochta.ru/specification#/enums-base-transport-type
        :param with_order_of_notice: Отметка 'С заказным уведомлением'
        :param with_simple_notice: Отметка 'С простым уведомлением'

        :return: Результат расчета доставки
        """
        url = '/1.0/tariff'
        data = {
            'completeness-checking': completeness_checking,
            'courier': courier,
            'declared-value': declared_value,
            'dimension': {
                'height': height,
                'length': length,
                'width': width,
            },
            'entries-type': entries_type,
            'fragile': fragile,
            'index-from': index_from,
            'index-to': index_to,
            'mail-category': mail_category,
            'mail-direct': mail_direct,
            'mail-type': mail_type,
            'mass': mass,
            'notice-payment-method': notice_payment_method,
            'payment-method': payment_method,
            'sms-notice-recipient': sms_notice_recipient,
            'transport-type': transport_type,
            'with-order-of-notice': with_order_of_notice,
            'with-simple-notice': with_simple_notice,
        }
        res = self._request('post', url, data=data)
        return res.json()

    # endregion
