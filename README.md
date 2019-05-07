fs-pochta-api
==========

Описание
------------
Библиотека для работы с API [Почты России](https://www.pochta.ru/support/business/api).

Установка
------------
Для работы требуется Python 3.6+
Для установки используйте [pipenv](http://pipenv.org/) (или pip):

```bash
$ pipenv install fs-pochta-api
$ pip install fs-pochta-api
```

Реализованные методы API
-----------
1. Трекинг (Модуль `pochta.tracking`)
    * [x] Единичный доступ
    * [ ] Пакетный доступ 
2. Доставка (Модуль `pochta.delivery`)
    * [ ] Заказы
    * [ ] Партии
    * [ ] Документы
    * [ ] Архив
    * [ ] Поиск ОПС
    * [ ] Долгосрочное хранение
    * [ ] Настройки
    * [x] Данные
    
Примеры
-------------
### Трекинг
Получение истории отправления
```python
tracker = Tracking('login', 'pass')
history = tracker.get_history('barcode')
```

### Доставка
#### Инициализация клиента
```python
delivery = Delivery('email', 'password','access_token')
```

#### Расчет стоимости доставки
```python
calc_result = delivery.calc_delivery(
    index_from='680000', # Индексы ОПС указанные в ЛК
    index_to='644015',
    mail_category=MailCategory.ORDINARY,
    mail_type=MailType.POSTAL_PARCEL,
    mass=1000,
    height=2,
    length=5,
    width=197,
    fragile=True
)
```

#### Нормализация адреса
```python
result = delivery.clean_address([
    Address("Москва, Варшавское шоссе, 37"),
    Address("ул. Мясницкая, д. 26, г. Москва, 1")
])
```

#### Получение баланса
```python
print(delivery.balance)
```

#### Нормализация ФИО
```python
print(delivery.clean_physical([Name('Иван Иванов Иванович')]))
```

#### Нормализация телефона
```python
print(delivery.clean_phone([Phone('+79999999999')]))
```

#### Неблагонадёжный получатель
```python
recipient = Recipient(
    address='Москва, ул. Пушкина 1, 1', 
    full_name='Иванов Иван Иванович', 
    phone='+79999999999',
)
print(delivery.check_unreliable_recipient([recipient]))
```