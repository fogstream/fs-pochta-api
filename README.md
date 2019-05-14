fs-pochta-api
==========

[![PyPI Version](https://img.shields.io/pypi/v/fs-pochta-api.svg)](https://pypi.python.org/pypi/fs-pochta-api)

Описание
------------
Библиотека для работы с API [Почты России](https://www.pochta.ru/support/business/api).

Документация
------------
[Ссылка](https://fogstream.github.io/fs-pochta-api/) на документацию библиотеки.

Установка библиотеки
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
    * [x] Заказы
    * [x] Партии
    * [x] Документы
    * [x] Архив
    * [x] Поиск ОПС
    * [x] Долгосрочное хранение
    * [x] Настройки
    * [x] Данные

