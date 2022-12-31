# gQiwiAPI by _Gnifajio_

![](https://badgen.net/badge/release/v1.4.2/grey) ![](https://komarev.com/ghpvc/?username=gnifajio-gQiwiAPI&label=views)

_A simple API for creating a payment link_

#### Installation

```sh
git clone https://github.com/gnifajio/gQiwiAPI.git
pip install -r requirements.txt
cd gQiwiAPI
python3 setup.py install
```

or

```sh
pip install gQiwiAPI
```

#### Usage

```python
# Initialization
from gQiwiAPI import Qiwi

SECRET_KEY = 'Your secret key for managing payments'
qiwi = Qiwi(SECRET_KEY)
# Creating a bill
my_first_bill = qiwi.new(10, '15m')
# Getting a payment link
payUrl = my_first_bill.payUrl
# Checking the payment status
bill_state = qiwi.status(my_first_bill)
# Checking the payment status by id
state_by_id = qiwi.check_id(my_first_bill.bill_id)
```

> You can get `SECRET_KEY` on [official website](https://qiwi.com/p2p-admin/transfers/api).

##### Syntax

```python
class Qiwi:
    def new(self, amount, comment=None, exp_dt='15m'): ...
```

> `amount` - the amount of the payment in rubles.
> `comment` - comment
> `expDT` - the validity time of the link.

About `amount` I will only say that you can pass `str`, `int` and `float` there and everything will work fine.

The default comment is set to `None`, and is not used.
You can add a comment to the payment like this:

``` python
qiwi.create_bill(self, 10, comment='Test', expDT='30m')
```

`expDT` is set in the format `nd:nh:nm:ns`, where

> `n` - int
> `d` - days
> `h` - hours
> `m` - minutes
> `s` - seconds

You can pass both integer and fractional numbers to `n`, the order is also not important.
For example:

```python
from gQiwiAPI import Qiwi

qiwi = Qiwi('SECRET_KEY')
amount = 10
qiwi.new(amount, exp_dt='0.3d:77m:0.5h')
```

#### Links

[QIWI: API of P2P accounts. Invoicing.](https://developer.qiwi.com/ru/p2p-payments/?shell#create)

[QIWI: Authentication data.](https://qiwi.com/p2p-admin/transfers/api)

#### TODO

- Expand the API
-
    - Add `customer` support
-
    - Add `customFields` support
