from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Optional

from requests import Response

from pochta.enums import PrintType
from pochta.utils import HTTPMethod


if TYPE_CHECKING:
    from pochta import Delivery


class Documents:
    """
    Методы API Документов.

    Используется через объект :class:`Delivery <pochta.delivery.Delivery>` или вручную.
    """

    def __init__(self, client: Delivery) -> None:
        """
        Инициализация API Документов.

        :param client: API клиент Доставки
        """
        self._client = client

    def create_all_docs(self, batch_name: str) -> Response:
        """
        Генерация пакета документации.

        Генерирует и возвращает zip архив с 4-мя файлами:
            - Export.xls , Export.csv - список с основными данными по заявкам в составе партии
            - F103.pdf - форма ф103 по заявкам в составе партии
            - В зависимости от типа и категории отправлений, формируется комбинация из
              сопроводительных документов в формате pdf ( формы: f7, f112, f22)

        https://otpravka.pochta.ru/specification#/documents-create_all_docs

        :param batch_name: Наименование партии
        :return: Ответ API
        """
        url = f'/1.0/forms/{batch_name}/zip-all'

        res = self._client.request(HTTPMethod.GET, url, stream=True)
        return res

    def create_f7_f22(self, shipment_id: str, sending_date: Optional[date] = None,
                      print_type: Optional[PrintType] = None) -> Response:
        """
        Генерация печатной формы Ф7п.

        Генерирует и возвращает pdf файл с формой ф7п для указанного заказа.
        Опционально в файл прикрепляется форма Ф22 (посылка онлайн).
        Если параметр sending-date не передается, берется текущая дата.

        https://otpravka.pochta.ru/specification#/documents-create_f7_f22

        :param shipment_id: Уникальный идентификатор заказа
        :param sending_date: Дата отправки в почтовое отделение (yyyy-MM-dd)
        :param print_type: Тип печати
        :return: Ответ API
        """
        url = f'/1.0/forms/{shipment_id}/f7pdf'

        if isinstance(sending_date, date):
            sending_date = sending_date.isoformat()

        params = {
            'sending-date': sending_date,
            'print-type': print_type,
        }

        res = self._client.request(HTTPMethod.GET, url, params=params, stream=True)
        return res

    def create_f112(self, shipment_id: str, sending_date: Optional[date] = None) -> Response:
        """
        Генерация печатной формы Ф112ЭК.

        Генерирует и возвращает pdf-файл с заполненной формой Ф112ЭК для указанного заказа.
        Только для заказа с «наложенным платежом». Если заказ не имеет данного атрибута,
        метод вернет ошибку. Если параметр sending-date не передается, берется текущая дата.

        https://otpravka.pochta.ru/specification#/documents-create_f112

        :param shipment_id: Уникальный идентификатор заказа
        :param sending_date: Дата отправки в почтовое отделение (yyyy-MM-dd)
        :return: Ответ API
        """
        url = f'/1.0/forms/{shipment_id}/f112pdf'

        if isinstance(sending_date, date):
            sending_date = sending_date.isoformat()

        params = {'sending-date': sending_date}

        res = self._client.request(HTTPMethod.GET, url, params=params, stream=True)
        return res

    def create_forms_backlog(self, shipment_id: str,
                             sending_date: Optional[date] = None) -> Response:
        """
        Генерация печатных форм для заказа (до формирования партии).

        Генерирует и возвращает pdf файл, который может содержать в зависимости от типа отправления:
            - форму ф7п (посылка, посылка-онлайн, бандероль, курьер-онлайн)
            - форму Е-1 (EMS, EMS-оптимальное, Бизнес курьер, Бизнес курьер экспресс)
            - конверт (письмо заказное)

        Опционально прикрепляются формы: Ф112ЭК (отправление с наложенным платежом),
        Ф22 (посылка онлайн), уведомление (для заказного письма или бандероли).

        https://otpravka.pochta.ru/specification#/documents-create_forms_backlog

        :param shipment_id: Уникальный идентификатор заказа
        :param sending_date: Дата отправки в почтовое отделение (yyyy-MM-dd)
        :return: Ответ API
        """
        url = f'/1.0/forms/backlog/{shipment_id}/forms'

        if isinstance(sending_date, date):
            sending_date = sending_date.isoformat()

        params = {'sending-date': sending_date}

        res = self._client.request(HTTPMethod.GET, url, params=params, stream=True)
        return res

    def create_forms(self, shipment_id: str, sending_date: Optional[date] = None,
                     print_type: Optional[PrintType] = None) -> Response:
        """
        Генерация печатных форм для заказа.

        Генерирует и возвращает pdf файл, который содержит, либо:
            - форму ф7п (посылка, посылка-онлайн, бандероль, курьер-онлайн)
            - форму Е-1 (EMS, EMS-оптимальное, Бизнес курьер, Бизнес курьер экспресс)
            - конверт (письмо заказное)

        Опционально прикрепляются формы: Ф112ЭК (отправление с наложенным платежом),
        Ф22 (посылка онлайн), уведомление и опись вложения (для заказного письма или бандероли).

        https://otpravka.pochta.ru/specification#/documents-create_forms

        :param shipment_id: Уникальный идентификатор заказа
        :param sending_date: Дата отправки в почтовое отделение (yyyy-MM-dd)
        :param print_type: Тип печати
        :return: Ответ API
        """
        url = f'/1.0/forms/{shipment_id}/forms'

        if isinstance(sending_date, date):
            sending_date = sending_date.isoformat()

        params = {
            'sending-date': sending_date,
            'print-type': print_type,
        }

        res = self._client.request(HTTPMethod.GET, url, params=params, stream=True)
        return res

    def create_f103(self, batch_name: str) -> Response:
        """
        Генерация печатной формы Ф103.

        Генерирует и возвращает pdf файл с формой Ф103 для указанной партии.

        https://otpravka.pochta.ru/specification#/documents-create_f103

        :param batch_name: Наименование партии
        :return: Ответ API
        """
        url = f'/1.0/forms/{batch_name}/f103pdf'

        res = self._client.request(HTTPMethod.GET, url, stream=True)
        return res

    def checkin(self, batch_name: str) -> dict:
        """
        Подготовка и отправка электронной формы Ф103.

        Присваивает уникальную версию партии для дальнейшего приема этой партии сотрудниками ОПС.
        Отправляет по e-mail электронную форму Ф103 в ОПС для регистрации.

        https://otpravka.pochta.ru/specification#/documents-checkin

        :param batch_name: Наименование партии
        :return: Результат операции
        """
        url = f'/1.0/batch/{batch_name}/checkin'

        res = self._client.request(HTTPMethod.GET, url)
        return res.json()

    def create_comp_check_form(self, batch_name: str) -> Response:
        """
        Генерация печатной формы акта осмотра содержимого.

        Генерирует и возвращает pdf файл с формой акта осмотра содержимого для указанной партии.

        https://otpravka.pochta.ru/specification#/documents-create_comp_check_form

        :param batch_name: Наименование партии
        :return: Ответ API
        """
        url = f'/1.0/forms/{batch_name}/completeness-checking-form'

        res = self._client.request(HTTPMethod.GET, url, stream=True)
        return res
