from enum import auto

from .utils import _AutoName


class EntryType(_AutoName):
    """
    Категория вложения.

    https://otpravka.pochta.ru/specification#/enums-base-entries-type
    """

    GIFT = auto()
    DOCUMENT = auto()
    SALE_OF_GOODS = auto()
    COMMERCIAL_SAMPLE = auto()
    OTHER = auto()


class MailCategory(_AutoName):
    """
    Категория РПО.

    https://otpravka.pochta.ru/specification#/enums-base-mail-category
    """

    SIMPLE = auto()
    ORDERED = auto()
    ORDINARY = auto()
    WITH_DECLARED_VALUE = auto()
    WITH_DECLARED_VALUE_AND_CASH_ON_DELIVERY = auto()
    COMBINED = auto()


class MailType(_AutoName):
    """
    Вид РПО.

    https://otpravka.pochta.ru/specification#/enums-base-mail-type
    """

    POSTAL_PARCEL = auto()
    ONLINE_PARCEL = auto()
    ONLINE_COURIER = auto()
    EMS = auto()
    EMS_OPTIMAL = auto()
    EMS_RT = auto()
    LETTER = auto()
    LETTER_CLASS_1 = auto()
    BANDEROL = auto()
    BUSINESS_COURIER = auto()
    BUSINESS_COURIER_ES = auto()
    PARCEL_CLASS_1 = auto()
    BANDEROL_CLASS_1 = auto()
    VGPO_CLASS_1 = auto()
    SMALL_PACKET = auto()
    COMBINED = auto()


class PaymentType(_AutoName):
    """
    Способы оплаты.

    https://otpravka.pochta.ru/specification#/enums-payment-methods
    """

    CASHLESS = auto()
    STAMP = auto()
    FRANKING = auto()
    TO_FRANKING = auto()
    ONLINE_PAYMENT_MARK = auto()


class TransportType(_AutoName):
    """
    Вид транспортировки.

    https://otpravka.pochta.ru/specification#/enums-base-transport-type
    """

    SURFACE = auto()
    AVIA = auto()
    COMBINED = auto()
    EXPRESS = auto()


class PrintType(_AutoName):
    """
    Тип печати (формат адресного ярлыка).

    https://otpravka.pochta.ru/specification#/enums-base-print-type
    """

    PAPER = auto()
    THERMO = auto()


class PostofficeWorkType(_AutoName):
    """Ограничение по времени работы для поиска ОПС."""

    ALL = auto()
    ROUND_THE_CLOCK = auto()
    CURRENTLY_WORKING = auto()
    WORK_ON_WEEKENDS = auto()


class AddressType(_AutoName):
    """
    Тип адреса.

    https://otpravka.pochta.ru/specification#/enums-base-address-type
    """

    DEFAULT = auto()
    PO_BOX = auto()
    DEMAND = auto()
    UNIT = auto()


class BatchCategory(_AutoName):
    """
    Категория партии.

    https://otpravka.pochta.ru/specification#/enums-base-batch-category
    """

    SIMPLE = auto()
    ORDERED = auto()
    ORDINARY = auto()
    WITH_DECLARED_VALUE = auto()
    WITH_DECLARED_VALUE_AND_CASH_ON_DELIVERY = auto()
    WITH_DECLARED_VALUE_AND_COMPULSORY_PAYMENT = auto()
    COMBINED = auto()


class EnvelopeType(_AutoName):
    """
    Тип конверта.

    https://otpravka.pochta.ru/specification#/enums-base-envelope-type
    """

    C4 = auto()
    C5 = auto()
    DL = auto()
    A6 = auto()
    A7 = auto()
