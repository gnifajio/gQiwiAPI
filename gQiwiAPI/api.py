import uuid
from datetime import datetime, timedelta
from typing import Dict, Union

import httpx
import pytz
from requests.exceptions import JSONDecodeError

__all__ = ['Qiwi', 'Bill']

URLTypes = Union["URL", str]
ProxiesTypes = Union[URLTypes, "Proxy", Dict[URLTypes, Union[None, URLTypes, "Proxy"]]]


class Bill:
    def __init__(self, resp: httpx.Response):
        try:
            rjson = resp.json()
        except JSONDecodeError as e:
            raise JSONDecodeError(resp.content, e.doc, e.pos) from e
        self._raw_data = resp.json()
        self.bill_id = rjson['billId']
        self.expDT = rjson['expirationDateTime']
        self.amount = rjson['amount']['value']
        self.payUrl = rjson['payUrl']

    def __repr__(self):
        return f'<Bill amount={self.amount}, id={self.bill_id}>'


class Qiwi:
    def __init__(self, secret_key: str, proxies: ProxiesTypes | None = None):
        self._SECRET_KEY = secret_key
        self._headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {self._SECRET_KEY}'
        }
        self._client = httpx.Client(base_url='https://api.qiwi.com/partner',
                                    headers=self._headers,
                                    proxies=proxies)
        try:
            self.new(1, exp_dt='1m')
        except Exception as e:
            raise ValueError('incorrect `secret_key`') from e

    def new(self, amount: str | int | float, comment: str = None, exp_dt: str | timedelta = '15m'):
        amount = self._format_amount(amount=amount)
        bill_id = str(uuid.uuid4())

        data = {
            'amount': {
                'currency': 'RUB',
                'value': f'{amount}'
            },
            "expirationDateTime": self._create_time(exp_dt),
        }

        if comment is not None:
            data['comment'] = comment

        resp = self._client.put(url=f'/bill/v1/bills/{bill_id}', json=data)

        return Bill(resp)

    def status(self, bill: Bill):
        return self.check_id(bill.bill_id)

    def check_id(self, pay_id: str):
        rjson = self._client.get(url=f'/bill/v1/bills/{pay_id}').json()
        try:
            return rjson['status']['value']
        except KeyError as e:
            raise ConnectionError(rjson) from e

    def _format_amount(self, amount: int | float | str):
        if isinstance(amount, float):
            return str(round(amount, 2)).ljust(len(str(round(amount))) + 3, '0')
        elif isinstance(amount, int):
            return str(amount) + '.00'
        elif isinstance(amount, str):
            return self._format_amount(float(amount))
        else:
            raise ValueError(f'`amount` must be `int`, `float` or `str`, not `{amount.__class__.__name__}`')

    @staticmethod
    def _create_time(time: str | timedelta, split: str = ':'):
        if isinstance(time, str):
            dtargs = {'days': 0,
                      'hours': 0,
                      'minutes': 0,
                      'seconds': 0}
            times = time.split(split)
            for i in times:
                code = i[-1]
                tm = float(i[:-1])
                if code == 'd':
                    dtargs['days'] += tm
                elif code == 'h':
                    dtargs['hours'] += tm
                elif code == 'm':
                    dtargs['minutes'] += tm
                elif code == 's':
                    dtargs['seconds'] += tm
                else:
                    raise ValueError(f'incorrect time {i!r}. Time code must be d/h/m/s, not {code!r}')
            return datetime.isoformat(datetime.now(pytz.timezone('Europe/Moscow')) +
                                      timedelta(**dtargs)).split('.')[0] + '+03:00'
        elif isinstance(time, timedelta):
            return datetime.isoformat(datetime.now(pytz.timezone('Europe/Moscow')) +
                                      time).split('.')[0] + '+03:00'
        else:
            raise ValueError(f'`time` must be `str` or `timedelta`, not `{time.__class__.__name__}`')
