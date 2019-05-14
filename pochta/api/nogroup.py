from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pochta.enums import (
    EntryType,
    MailCategory,
    MailType,
    PaymentType,
    TransportType,
)
from pochta.helpers import Address, Name, Phone, Recipient
from pochta.utils import HTTPMethod


if TYPE_CHECKING:
    from pochta import Delivery


class NoGroup:
    """
    Методы API Данных.

    Используется через объект :class:`Delivery <pochta.delivery.Delivery>` или вручную.
    """

    def __init__(self, client: Delivery):
        """
        Инициализация API Данных.

        :param client: API клиент Доставки
        """
        self._client = client

    def address_normalization(self, addresses: List[Address]) -> dict:
        """
        Нормализация адреса.

        Разделяет и помещает сущности переданных адресов (город, улица)
        в соответствующие поля возвращаемого объекта.
        Параметр id (идентификатор записи) используется для установления
        соответствия переданных и полученных записей, так как порядок
        сортировки возвращаемых записей не гарантируется.
        Метод автоматически ищет и возвращает индекс близлежащего
        ОПС по указанному адресу.

        https://otpravka.pochta.ru/specification#/nogroup-normalization_adress

        :param addresses:  Список адрессов
        :return: Результат нормализации
        """
        url = f'/1.0/clean/address'

        data = [address.raw for address in addresses]

        res = self._client.request(HTTPMethod.POST, url, data=data)
        return res.json()

    def fio_normalization(self, names: List[Name]) -> dict:
        """
        Нормализация ФИО.

        Очищает, разделяет и помещает значения ФИО в соответствующие
        поля возвращаемого объекта. Параметр id (идентификатор записи)
        используется для установления соответствия переданных и полученных
        записей, так как порядок сортировки возвращаемых
        записей не гарантируется.

        https://otpravka.pochta.ru/specification#/nogroup-normalization_fio

        :param names: Список имен
        :return: Результат нормализации
        """
        url = f'/1.0/clean/physical'

        data = [name.raw for name in names]

        res = self._client.request(HTTPMethod.POST, url, data=data)
        return res.json()

    def phone_normalization(self, phone_numbers: List[Phone]) -> dict:
        """
        Нормализация телефона.

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

        https://otpravka.pochta.ru/specification#/nogroup-normalization_phone

        :param phone_numbers: Список номеров
        :return: Результат нормализации
        """
        url = '/1.0/clean/phone'

        data = [phone.raw for phone in phone_numbers]

        res = self._client.request(HTTPMethod.POST, url, data=data)
        return res.json()

    def check_reliability(self, recipients: List[Recipient]) -> List[dict]:
        """
        Проверка благонадежности получателя.

        Актуально для отправлений с наложенным платежом.
        Определяет, является ли получатель благонадёжным, есть ли прецеденты невыкупа.

        https://otpravka.pochta.ru/specification#/nogroup-unreliable_recipient

        :param recipients: Список получателей
        :return: Результат проверки
        """
        url = '/1.0/unreliable-recipient'

        data = [recipient.raw for recipient in recipients]

        res = self._client.request(HTTPMethod.POST, url, data=data)
        return res.json()

    @property
    def counterpart_balance(self) -> dict:
        """
        Отображение баланса.

        Отображает баланс расчетного счета. Возвращаемые значения указываются в копейках.

        https://otpravka.pochta.ru/specification#/nogroup-counterpart_balance

        :return: Информация о балансе контрагента
        """
        url = '/1.0/counterpart/balance'

        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    def calc_delivery_rate(self, completeness_checking: Optional[bool] = None,
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
                           with_simple_notice: bool = False) -> dict:
        """
        Калькулятор стоимости доставки.

        Рассчитывает стоимость пересылки в зависимости от указанных
        входных данных. Индекс ОПС точки отправления берется из профиля
        клиента. Возвращаемые значения указываются в копейках.

        https://otpravka.pochta.ru/specification#/nogroup-rate_calculate

        :param completeness_checking: Признак услуги проверки комплектности
        :param courier: Отметка "Курьер"
        :param declared_value: Объявленная ценность
        :param height: Линейная высота (сантиметры)
        :param length: Линейная длина (сантиметры)
        :param width: Линейная ширина (сантиметры)
        :param entries_type: Категория вложения.
        :param fragile: Отметка "Осторожно/Хрупко"
        :param index_from: Почтовый индекс объекта почтовой связи места приема
        :param index_to: Почтовый индекс объекта почтовой связи места назначения
        :param mail_category: Категория РПО
        :param mail_direct: Код страны назначения.
        :param mail_type: Вид РПО
        :param mass: Масса отправления в граммах
        :param notice_payment_method: Способ оплаты уведомеления.
        :param payment_method: Способ оплаты.
        :param sms_notice_recipient: Признак услуги SMS уведомления
        :param transport_type: Вид транспортировки
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

        res = self._client.request(HTTPMethod.POST, url, data=data)
        return res.json()
