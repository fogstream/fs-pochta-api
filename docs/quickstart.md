Использование
===============

Трекинг
----------

[Документация API Трекинга](https://tracking.pochta.ru/specification)

```python
from pochta import Tracking

tracking = Tracking('login', 'password')

history = tracking.get_history('barcode')
print(history)
```

Отправка
-----------

[Документация API Отправки](https://otpravka.pochta.ru/specification)

#### Создание отправления
```python
from pochta import Delivery
from pochta.enums import AddressType, TransportType
from pochta.helpers import Order

delivery = Delivery('login', 'password', 'token')

order = Order(
    mass=1000,
    order_num='af134qrw124gva',
    fragile=True,
)
order.set_address(
    address_type_to=AddressType.DEFAULT,
    house_to='37',
    index_to=117105,
    mail_direct=643,
    place_to='г Москва',
    postoffice_code=101000,
    region_to='г Москва',
    street_to='ш Варшавское',
    transport_type=TransportType.SURFACE,
)
order.set_recipient(
    given_name='Иван',
    surname='Иванов',
    middle_name='Иванович',
    tel_address=79459562067,
)
order.set_dimensions(
    height=3,
    length=9,
    width=73,
)

new_shipments = delivery.orders.create_order([order])
new_batch = delivery.batches.create_batch(new_shipments['result_ids'][0])
```

#### Расчет стоимости доставки
```python
from pochta import Delivery
from pochta.enums import MailCategory, MailType

delivery = Delivery('login', 'password', 'token')
calc_result = delivery.nogroup.calc_delivery_rate(
    index_from='680000', # Индексы ОПС указанные в ЛК
    index_to='644015',
    mail_category=MailCategory.ORDINARY,
    mail_type=MailType.POSTAL_PARCEL,
    mass=1000,
    height=2,
    length=5,
    width=197,
    fragile=True,
)
```

#### Нормализация адреса
```python
from pochta import Delivery
from pochta.helpers import Address

delivery = Delivery('login', 'password', 'token')

result = delivery.nogroup.address_normalization([
    Address("Москва, Варшавское шоссе, 37"),
    Address("ул. Мясницкая, д. 26, г. Москва, 1")
])
```

#### Нормализация ФИО
```python
from pochta import Delivery
from pochta.helpers import Name

delivery = Delivery('login', 'password', 'token')

result = delivery.nogroup.fio_normalization([Name('Иван Иванов Иванович')])
```

#### Нормализация телефона

```python
from pochta import Delivery
from pochta.helpers import Phone

delivery = Delivery('login', 'password', 'token')

phone_1 = Phone('+79999999999')
phone_2 = Phone('+79099999999')
# ID необходим для установления нужного номера из ответа API если номеров несколько
phone_1_id = phone_1.id
print(delivery.nogroup.phone_normalization([phone_1, phone_2]))
```

#### Проверка благонадежности получателя
```python
from pochta import Delivery
from pochta.helpers import Recipient

delivery = Delivery('login', 'password', 'token')

recipient = Recipient(
    address='Москва, ул. Пушкина 1, 1',
    full_name='Иванов Иван Иванович',
    phone='+79999999999',
)

print(delivery.nogroup.check_reliability([recipient]))
```

#### Получение баланса
```python
from pochta import Delivery

delivery = Delivery('login', 'password', 'token')

print(delivery.nogroup.counterpart_balance)
```
