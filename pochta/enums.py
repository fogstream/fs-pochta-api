from enum import auto

from .utils import _AutoName


class EntryType(_AutoName):
    GIFT = auto()
    DOCUMENT = auto()
    SALE_OF_GOODS = auto()
    COMMERCIAL_SAMPLE = auto()
    OTHER = auto()


class MailCategory(_AutoName):
    SIMPLE = auto()
    ORDERED = auto()
    ORDINARY = auto()
    WITH_DECLARED_VALUE = auto()
    WITH_DECLARED_VALUE_AND_CASH_ON_DELIVERY = auto()
    COMBINED = auto()


class MailType(_AutoName):
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
    CASHLESS = auto()
    STAMP = auto()
    FRANKING = auto()
    TO_FRANKING = auto()
    ONLINE_PAYMENT_MARK = auto()


class TransportType(_AutoName):
    SURFACE = auto()
    AVIA = auto()
    COMBINED = auto()
    EXPRESS = auto()
