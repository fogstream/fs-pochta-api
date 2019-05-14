from typing import List, Optional, Union

from .enums import (
    AddressType,
    EntryType,
    EnvelopeType,
    MailCategory,
    MailType,
    PaymentType,
    TransportType,
)
from .utils import _UniqId


class Address(_UniqId):
    def __init__(self, address: str):
        """
        Адрес для нормализации.

        :param address: Оригинальный адрес одной строкой
        """
        super().__init__()
        self.address = address

    @property
    def raw(self) -> dict:
        """Получения словаря для отправки через API."""
        return {'id': self.id, 'original-address': self.address}

    def __str__(self):
        """Адрес."""
        return self.address


class Name(_UniqId):
    def __init__(self, name: str):
        """
        ФИО для нормализации.

        :param name: Оригинальные фамилия, имя , отчество одной строкой
        """
        super().__init__()
        self.name = name

    @property
    def raw(self) -> dict:
        """Получения словаря для отправки через API."""
        return {'id': self.id, 'original-fio': self.name}

    def __str__(self) -> str:
        """Имя."""
        return self.name


class Phone(_UniqId):
    def __init__(self, phone: str,
                 area: Optional[str] = None,
                 place: Optional[str] = None,
                 region: Optional[str] = None):
        """
        Телефон для нормализации.

        :param phone: Оригинальный номер одной строкой
        :param area: Область/край трелефонного номера
        :param place: Город телефонного номера
        :param region: Регион телефонного номера
        """
        super().__init__()
        self.phone = phone
        self.area = area
        self.place = place
        self.region = region

    @property
    def raw(self) -> dict:
        """Получения словаря для отправки через API."""
        return {
            'id': self.id,
            'original-phone': self.phone,
            'area': self.area,
            'place': self.place,
            'region': self.region,
        }

    def __str__(self) -> str:
        """Номер телефона."""
        return self.phone


class Recipient(_UniqId):
    def __init__(self, address: str, full_name: str, phone: str):
        """
        Получатель для проверки благонадежности.

        :param address: Адрес
        :param full_name: Полное имя
        :param phone: Телефон
        """
        super().__init__()
        self.address = address
        self.full_name = full_name
        self.phone = phone

    @property
    def raw(self) -> dict:
        """Получения словаря для отправки через API."""
        return {
            'raw-address': self.address,
            'raw-full-name': self.full_name,
            'raw-telephone': self.phone,
        }

    def __str__(self):
        """Полное имя (ФИО)."""
        return self.full_name


class Item:
    """Вложение."""

    def __init__(self, description: str,
                 quantity: int,
                 value: Optional[int] = None,
                 vat_rate: Optional[int] = None,
                 insurance_value: Optional[int] = None) -> None:
        """
        Конструктор вложения.

        :param description: Наименование товара
        :param quantity: Количество товара
        :param value: Цена товара (вкл. НДС)
        :param vat_rate: Ставка НДС
        :param insurance_value: Объявленная ценность
        """
        self.description = description
        self.quantity = quantity
        self.value = value
        self.vat_rate = vat_rate
        self.insurance_value = insurance_value

    @property
    def raw(self) -> dict:
        """
        Представление Вложения для использования в конструкторе РПО.

        :return: Словарь с данными Вложения
        """
        return {
            'description': self.description,
            'quantity': self.quantity,
            'value': self.value,
            'insr-value': self.insurance_value,
            'vat-rate': self.vat_rate,
        }

    def __str__(self):
        """Строковое представление."""
        return f'{self.description} [{self.value} x {self.quantity}]'


class CustomsEntry:
    """Вложение."""

    def __init__(self, amount: int, country_code: int,
                 description: str, tnved_code: str,
                 weight: int, value: Optional[int] = None) -> None:
        """
        Конструктор вложения.

        :param amount: Количество
        :param country_code: Код страны происхождения.
        :param description: Наименование товара
        :param tnved_code: Код ТНВЭД
        :param weight: Вес вложения в граммах
        :param value: Цена товара (вкл. НДС)
        """
        self.amount = amount
        self.country_code = country_code
        self.description = description
        self.tnved_code = tnved_code
        self.weight = weight
        self.value = value

    @property
    def raw(self) -> dict:
        """
        Представление Таможенного Вложения для использования в конструкторе РПО.

        :return: Словарь с данными Вложения
        """
        return {
            'amount': self.amount,
            'country-code': self.country_code,
            'description': self.description,
            'tnved-code': self.tnved_code,
            'value': self.value,
            'weight': self.weight,
        }

    def __str__(self):
        """Строковое представление."""
        return f'{self.description} [{self.amount}]'


# pylint: disable=R0902
class Order:
    """Класс помошник создания РПО."""

    def __init__(self, mass: int, order_num: str, fragile: bool,
                 mail_category: MailCategory = MailCategory.SIMPLE,
                 mail_type: MailType = MailType.POSTAL_PARCEL,
                 payment: Optional[int] = None,
                 payment_method: Optional[PaymentType] = None) -> None:
        """
        Инициализация РПО.

        https://otpravka.pochta.ru/specification#/orders-creating_order

        :param mass: Вес РПО (в граммах).
        :param order_num: Номер заказа. Внешний идентификатор заказа,
            который формируется отправителем.
        :param fragile: Установлена ли отметка "Осторожно/Хрупкое"?
        :param mail_category: Категория РПО.
        :param mail_type: Вид РПО.
        :param payment: Сумма наложенного платежа (копейки).
        :param payment_method: Способ оплаты.
        """
        self.mass = mass
        self.order_num = order_num
        self.fragile = fragile
        self.mail_category = mail_category
        self.mail_type = mail_type
        self.payment = payment
        self.payment_method = payment_method

        # region Получатель
        self.recipient_name = None
        self.given_name = None
        self.surname = None
        self.middle_name = None
        self.tel_address = None
        # endregion

        # region Адрес
        self.house_to = None
        self.mail_direct = None
        self.region_to = None
        self.place_to = None
        self.street_to = None
        self.address_type_to = None
        self.index_to = None
        self.postoffice_code = None
        self.area_to = None
        self.building_to = None
        self.hotel_to = None
        self.corpus_to = None
        self.slash_to = None
        self.letter_to = None
        self.location_to = None
        self.office_to = None
        self.room_to = None
        self.num_address_type_to = None
        self.raw_address = None
        self.str_index_to = None
        self.vladenie_to = None
        self.transport_type = None
        # endregion

        # region Таможенные декларация
        self.customs = False
        self.customs_currency = None
        self.customs_entries = None
        self.customs_entries_type = None
        self.customs_with_certificate = None
        self.customs_with_invoice = None
        self.customs_with_license = None
        # endregion

        # region Габариты
        self.dimensions = None
        # endregion

        # region Вложения
        self.items = None
        # endregion

        # region Дополнительные параметры РПО
        self.completeness_checking = None
        self.courier = None
        self.envelope_type = None
        self.delivery_with_cod = None
        self.insurance_value = None
        self.inventory = None
        self.no_return = None
        self.with_order_of_notice = None
        self.with_simple_notice = None
        self.sms_notice_recipient = None
        self.notice_payment_method = None
        self.wo_mail_rank = None
        # endregion

    def set_recipient(self, given_name: str, surname: str,
                      middle_name: Optional[str] = None,
                      recipient_name: Optional[str] = None,
                      tel_address: Optional[int] = None) -> None:
        """
        Указать получателя.

        :param recipient_name: Наименование получателя одной строкой (ФИО, наименование организации)
        :param given_name: Имя получателя
        :param surname: Фамилия получателя
        :param middle_name: Отчество получателя
        :param tel_address: Телефон получателя (может быть обязательным для
            некоторых типов отправлений)
        """
        self.recipient_name = recipient_name
        self.given_name = given_name
        self.surname = surname
        self.middle_name = middle_name
        self.tel_address = tel_address

    def set_address(self, house_to: str, mail_direct: int,
                    region_to: str, place_to: str, street_to: str,
                    address_type_to: AddressType = AddressType.DEFAULT,
                    index_to: Optional[Union[str, int]] = None,
                    postoffice_code: Optional[Union[str, int]] = None,
                    area_to: Optional[str] = None,
                    building_to: Optional[str] = None,
                    hotel_to: Optional[str] = None,
                    corpus_to: Optional[str] = None,
                    slash_to: Optional[str] = None,
                    letter_to: Optional[str] = None,
                    location_to: Optional[str] = None,
                    office_to: Optional[str] = None,
                    room_to: Optional[str] = None,
                    num_address_type_to: Optional[str] = None,
                    raw_address: Optional[str] = None,
                    str_index_to: Optional[str] = None,
                    vladenie_to: Optional[str] = None,
                    transport_type: Optional[TransportType] = None) -> None:
        """
        Установка адресных данных РПО.

        :param house_to: Часть адреса: Номер здания
        :param mail_direct: Код страны.
        :param region_to: Область, регион
        :param place_to: Населенный пункт
        :param street_to: Часть адреса: Улица
        :param address_type_to: Тип адреса.
        :param index_to: Почтовый индекс
        :param postoffice_code: Индекс места приема
        :param area_to: Район
        :param building_to: Часть здания: Строение
        :param hotel_to: Название гостиницы
        :param corpus_to: Часть здания: Корпус
        :param slash_to: Часть здания: Дробь
        :param letter_to: Часть здания: Литера
        :param location_to: Микрорайон
        :param office_to: Часть здания: Офис
        :param room_to: Часть здания: Номер помещения
        :param num_address_type_to: Номер для а/я, войсковая часть,
            войсковая часть ЮЯ, полевая почта
        :param raw_address: Необработанный адрес получателя
        :param str_index_to: Почтовый индекс (буквенно-цифровой)
        :param vladenie_to: Часть здания: Владение
        :param transport_type: Возможный вид транспортировки (для международных отправлений).
        """
        self.house_to = house_to
        self.mail_direct = mail_direct
        self.region_to = region_to
        self.place_to = place_to
        self.street_to = street_to
        self.address_type_to = address_type_to
        self.index_to = index_to
        self.postoffice_code = postoffice_code
        self.area_to = area_to
        self.building_to = building_to
        self.hotel_to = hotel_to
        self.corpus_to = corpus_to
        self.slash_to = slash_to
        self.letter_to = letter_to
        self.location_to = location_to
        self.office_to = office_to
        self.room_to = room_to
        self.num_address_type_to = num_address_type_to
        self.raw_address = raw_address
        self.str_index_to = str_index_to
        self.vladenie_to = vladenie_to
        self.transport_type = transport_type

    def add_customs_declaration(self, currency: str, entries_type: EntryType,
                                customs_entries: List[CustomsEntry],
                                with_certificate: Optional[bool] = None,
                                with_invoice: Optional[bool] = None,
                                with_license: Optional[bool] = None) -> None:
        """
        Таможенная декларация (для международных отправлений).

        :param currency: Код валюты.
        :param entries_type: Категория вложения.
        :param customs_entries: Список вложений
        :param with_certificate: Приложенные документы: сертификат
        :param with_invoice: Приложенные документы: счет-фактура
        :param with_license: Приложенные документы: лицензия
        """
        self.customs = True

        self.customs_currency = currency
        self.customs_entries = customs_entries
        self.customs_entries_type = entries_type
        self.customs_with_certificate = with_certificate
        self.customs_with_invoice = with_invoice
        self.customs_with_license = with_license

    def set_dimensions(self, height: int, length: int, width: int) -> None:
        """
        Добавление линейных размеров.

        :param height: Линейная высота (сантиметры)
        :param length: Линейная длина (сантиметры)
        :param width: Линейная ширина (сантиметры)
        """
        self.dimensions = {
            'height': height,
            'length': length,
            'width': width,
        }

    def add_items(self, items: List[Item]) -> None:
        """
        Добавление товарных вложений РПО.

        :param items: Список вложений
        """
        if not items:
            self.items = items
        else:
            self.items.extend(items)

    def add_services(self, completeness_checking: Optional[bool] = None,
                     courier: Optional[bool] = None,
                     envelope_type: Optional[EnvelopeType] = None,
                     delivery_with_cod: Optional[bool] = False,
                     insurance_value: Optional[int] = None,
                     inventory: Optional[bool] = None,
                     no_return: Optional[bool] = None,
                     with_order_of_notice: Optional[bool] = None,
                     with_simple_notice: Optional[bool] = None,
                     sms_notice_recipient: Optional[int] = None,
                     notice_payment_method: Optional[PaymentType] = None,
                     wo_mail_rank: Optional[bool] = None) -> None:
        """
        Дополнительные параметры РПО.

        :param completeness_checking: Признак услуги проверки комплектности.
        :param courier: Отметка "Курьер"
        :param envelope_type: Тип конверта - ГОСТ Р 51506-99.
        :param delivery_with_cod: Признак оплаты при получении.
        :param insurance_value: Объявленная ценность
        :param inventory: Наличие описи вложения
        :param no_return: Отметка "Возврату не подлежит"
        :param with_order_of_notice: Отметка 'С заказным уведомлением'
        :param with_simple_notice: Отметка 'С простым уведомлением'
        :param sms_notice_recipient: Признак услуги SMS уведомления
        :param notice_payment_method: Способ оплаты уведомления
        :param wo_mail_rank: Отметка "Без разряда"
        """
        self.completeness_checking = completeness_checking
        self.courier = courier
        self.envelope_type = envelope_type
        self.delivery_with_cod = delivery_with_cod
        self.insurance_value = insurance_value
        self.inventory = inventory
        self.no_return = no_return
        self.with_order_of_notice = with_order_of_notice
        self.with_simple_notice = with_simple_notice
        self.sms_notice_recipient = sms_notice_recipient
        self.notice_payment_method = notice_payment_method
        self.wo_mail_rank = wo_mail_rank

    @property
    def raw(self) -> dict:
        """
        Представление РПО для использования в вызовах API.

        :return: Словарь с данными РПО
        """
        if self.customs:
            customs_entries = [entry.raw for entry in self.customs_entries]
            customs_declaration = {
                'currency': self.customs_currency,
                'customs-entries': customs_entries,
                'entries=type': self.customs_entries_type,
                'with-certificate': self.customs_with_certificate,
                'with-invoice': self.customs_with_invoice,
                'with-license': self.customs_with_license,
            }
        else:
            customs_declaration = None

        if self.items:
            items = {'items': [item.raw for item in self.items]}
        else:
            items = None

        return {
            'address-type-to': self.address_type_to,
            'area-to': self.area_to,
            'building-to': self.building_to,
            'corpus-to': self.corpus_to,
            'completeness-checking': self.completeness_checking,
            'courier': self.courier,
            'customs-declaration': customs_declaration,
            'delivery-with-cod': self.delivery_with_cod,
            'dimension': self.dimensions,
            'envelope-type': self.envelope_type,
            'fragile': self.fragile,
            'given-name': self.given_name,
            'goods': items,
            'hotel-to': self.hotel_to,
            'house-to': self.house_to,
            'index-to': self.index_to,
            'insr-value': self.insurance_value,
            'inventory': self.inventory,
            'letter-to': self.letter_to,
            'location-to': self.location_to,
            'mail-category': self.mail_category,
            'mail-direct': self.mail_direct,
            'mail-type': self.mail_type,
            'mass': self.mass,
            'middle-name': self.middle_name,
            'no-return': self.no_return,
            'notice-payment-method': self.notice_payment_method,
            'num-address-type-to': self.num_address_type_to,
            'office-to': self.office_to,
            'order-num': self.order_num,
            'payment': self.payment,
            'payment-method': self.payment_method,
            'place-to': self.place_to,
            'postoffice-code': self.postoffice_code,
            'raw-address': self.raw_address,
            'recipient-name': self.recipient_name,
            'region-to': self.region_to,
            'room-to': self.room_to,
            'slash-to': self.slash_to,
            'sms-notice-recipient': self.sms_notice_recipient,
            'str-index-to': self.str_index_to,
            'street-to': self.street_to,
            'surname': self.surname,
            'tel-address': self.tel_address,
            'transport-type': self.transport_type,
            'vladenie-to': self.vladenie_to,
            'with-order-of-notice': self.with_order_of_notice,
            'with-simple-notice': self.with_simple_notice,
            'wo-mail-rank': self.wo_mail_rank,
        }
