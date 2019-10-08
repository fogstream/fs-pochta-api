from abc import ABC
from typing import List

from zeep import CachingClient, Client, Settings

from .exceptions import APIError


class _BaseClient(ABC):
    """API клиент сервиса отслеживания посылок.

    https://tracking.pochta.ru/specification
    """

    WSDL = ''

    def __init__(self, login: str, password: str, caching=True):
        """Инициализация API клиента сервиса отслеживания посылок.

        :param login: Логин от системы трекинга
        :param password: Пароль от системы трекинга
        :param caching: Флаг, позволяющий отключить кэширование в zeep
        """
        self._login = login
        self._password = password

        zeep_client = CachingClient if caching else Client

        self._client = zeep_client(
            self.WSDL,
            settings=Settings(strict=False),
        )


class SingleTracker(_BaseClient):
    """Клиент для взаимодеействия с API единичной обработки запросов."""

    WSDL = 'https://tracking.russianpost.ru/rtm34?wsdl'

    def get_history(self, barcode: str) -> dict:
        """
        История операций над отправлением.

        Метод getOperationHistory используется для получения информации о
        конкретном отправлении. Метод возвращает подробную информацию
        по всем операциям, совершенным над отправлением.

        https://tracking.pochta.ru/specification#getOperationHistory

        :param barcode: Идентификатор регистрируемого почтового отправления в одном из форматов:
            - внутрироссийский, состоящий из 14 символов (цифровой)
            - международный, состоящий из 13 символов (буквенно-цифровой) в формате S10.
        :return: Ответ метода getOperationHistory содержит список элементов
            historyRecord. Каждый из них содержит информацию об одной операции над
            отправлением. Если над отправлением еще не зарегистрировано ни одной
            операции, то возвращается пустой список элементов historyRecord.
        """
        return self._client.service.getOperationHistory(
            OperationHistoryRequest={
                'Barcode': barcode,
                'MessageType': '0'
            },
            AuthorizationHeader={
                'login': self._login,
                'password': self._password,
            },
        )

    def get_order_events_for_mail(self, barcode: str) -> dict:
        """
        История операций с наложенным платежом.

        Метод PostalOrderEventsForMail позволяет получить информацию об операциях с
        наложенным платежом, который связан с конкретным почтовым отправлением.

        https://tracking.pochta.ru/specification#PostalOrderEventsForMail

        :param barcode: Идентификатор регистрируемого почтового отправления в одном из форматов:
            - внутрироссийский, состоящий из 14 символов (цифровой);
            - международный, состоящий из 13 символов (буквенно-цифровой) в формате S10.
        :return: Список событий
        """
        return self._client.service.PostalOrderEventsForMail(
            PostalOrderEventsForMailInput={
                'Barcode': barcode,
            },
            AuthorizationHeader={
                'login': self._login,
                'password': self._password,
            },
        )


class BatchTracker(_BaseClient):
    """Клиент для взаимодеействия с API пакетной обработки запросов."""

    WSDL = 'https://tracking.russianpost.ru/fc?wsdl'

    def get_ticket(self, barcodes: List[str]) -> str:
        """Получения билета на подготовку информации по списку идентификаторов отправлений.

        Метод getTicket используется для получения билета
        на подготовку информации по списку идентификаторов отправлений.
        В запросе передается список идентификаторов отправлений.
        При успешном вызове метод возвращает идентификатор билета.

        Ограничения и рекомендации по использованию:
            - Количество идентификаторов отправлений в одном запросе не должно превышать *3000*.
            - Рекомендуется выполнять первое обращение за ответом по билету не ранее,
              чем через 15 минут от момента выдачи билета.
            - В случае неготовности результата повторные обращения по тому же билету следует
              выполнять не чаще, чем 1 раз в 15 минут
            - Время хранения ответа по билету в Сервисе отслеживания составляет 32 часа.
              По истечении этого периода ответ удаляется.

        https://tracking.pochta.ru/specification раздел "Пакетная обработка" п.3

        :param barcodes: Идентификаторы регистрируемых почтовогых отправлений в одном из форматов:
            - внутрироссийский, состоящий из 14 символов (цифровой)
            - международный, состоящий из 13 символов (буквенно-цифровой) в формате S10.
        :return: Ответ метода getTicket содержит информацию о выданном билете в объекте
            ticketResponse в случае успешного запроса, функция возвращает номер созданного ticket,
            полученного из ticketResponse.value
        """
        # По умолчанию zeep генерирует Request старой версии,
        # где запрос отправляется в виде файла с метаданными
        # Поэтому, вручную создаём объект Request  и убираем аттрибуты, относящиеся к файлу
        request = self._client.get_type('{http://fclient.russianpost.org}file')
        request.attributes.clear()

        items = [{'Barcode': barcode} for barcode in barcodes]

        response = self._client.service.getTicket(
            request=request(Item=items),
            login=self._login,
            password=self._password,
            language='RUS',
        )

        if response['error'] is not None:
            raise APIError(f'Response body contains error: {response["error"]}')

        return response['value']

    def get_response_by_ticket(self, ticket: str) -> List[dict]:
        """Метод используется для получения информации об отправлениях по ранее полученному билету.

        Вызывает метод answerByTicketRequest используемый для получения информации
        об отправлениях по ранее полученному билету.

        https://tracking.pochta.ru/specification раздел "Пакетная обработка" п.4

        :param ticket: Строка, содержащая номер ticket, полученного ранее при вызове getTicket
        :return: Результаты пакетной обработки в виде списка словарей,
            содержащих результаты выполнения запроса на пакетную обработку
        """
        response = self._client.service.getResponseByTicket(
            ticket=ticket,
            login=self._login,
            password=self._password,
        )

        if response['error'] is not None:
            raise APIError(f'Response body contains error: {response["error"]}')

        return response['value']['Item']
