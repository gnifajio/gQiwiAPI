# gQiwiAPI by _Gnifajio_ ![]() ![]() ![](https://badgen.net/badge/release/v1.0/grey)

_Простое API для создания ссылки на оплату_

#### Установка

[]()

```sh
git clone https://github.com/gnifajio/gQiwiAPI.git
pip install -r requirements.txt
```

#### Использование

[]()

```python
# Инициализация
from gQiwiAPI import Qiwi
SECRET_KEY = 'Ваш секретный ключ для управления платежами'
qiwi = Qiwi(SECRET_KEY)
# Создание счета
my_first_bill = qiwi.create_bill(10, '15m')
# Получение ссылки
payUrl = my_first_bill.payUrl
# Проверка статуса платежа
bill_state = qiwi.bill_status(my_first_bill)
```

> Получить `SECRET_KEY` можно на [офф. сайте](https://qiwi.com/p2p-admin/transfers/api).

##### Синтаксис

[]()

```python
qiwi.create_bill(self, amount, comment=None, expDT='15m')
```

> `amount` - сумма платежа в рублях.
> `comment` - комментарий.
> `expDT` - время валидности ссылки.

Про `amount` скажу только, что Вы можете передать туда `str`, `int` и `float` и все будет прекрасно работать.
[]()
Коментарий по умолчаниу установлен в значение `None`, и не используется.
Добавить комментарий к платежу можно так:
``` python
qiwi.create_bill(self, 10, comment='Тест', expDT='30m')
```
[]()
`expDT` задается в формате `nd:nh:nm:ns`, где

> `n` - число
> `d` - дни
> `h` - часы
> `m` - минуты
> `s` - секунды

Можно передавать в `n` как целое так и дробное число, порядок также не важен.
Например:
```python
amount = 10
qiwi.create_bill(amount, expDT='0.3d:77m:0.5h')
```

#### Ссылки

[QIWI: API P2P-счетов. Выставление счета](https://developer.qiwi.com/ru/p2p-payments/?shell#create)
[QIWI: Аутентификационные данные](https://qiwi.com/p2p-admin/transfers/api)

#### TODO

- Расширить API
- - Добавить поддержку customer.
- - Добавить поддержку customFields.
