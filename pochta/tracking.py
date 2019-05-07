from typing import Dict

from zeep import CachingClient, Settings


class Tracking:
    def __init__(self, login: str, password: str):
        """
        :param login: Логин от системы трекинга
        :param password: Пароль от системы трекинга
        """
        self._login = login
        self._password = password

        self._client = CachingClient(
            'https://tracking.russianpost.ru/rtm34?wsdl',
            settings=Settings(strict=False),
        )

    def get_history(self, barcode: str) -> Dict:
        """
        Метод getOperationHistory используется для получения информации о
        конкретном отправлении. Метод возвращает подробную информацию
        по всем операциям, совершенным над отправлением.
        :param barcode: Идентификатор регистрируемого почтового отправления
        в одном из форматов:
            - внутрироссийский, состоящий из 14 символов (цифровой);
            - международный, состоящий из 13 символов (буквенно-цифровой)
            в формате S10.
        :return: Ответ метода getOperationHistory содержит список элементов
        historyRecord. Каждый из них содержит информацию об одной операции над
        отправлением. Если над отправлением еще не зарегистрировано ни одной
        операции, то возвращается пустой список элементов historyRecord.
        По каждой операции в ответе обязательно присутствует следующая информация:
            - Дата операции (OperDate);
            - Место проведения операции (OperationAddress);
            - Операция (OperType) и ее атрибут (OperAttr).
        Прочая информация возвращается при её наличии в Сервисе отслеживания.
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
