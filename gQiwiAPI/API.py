import uuid
from datetime import datetime, timedelta

import pytz
import requests
from requests.exceptions import JSONDecodeError


class Bill:
    def __init__(self, resp: requests.Response):
        try:
            rjson = resp.json()
        except JSONDecodeError as e:
            raise JSONDecodeError(resp.content, e.doc, e.pos) from e

        self.bill_id = rjson['billId']
        self.expDT = rjson['expirationDateTime']
        self.amount = rjson['amount']['value']
        self.status = rjson['status']['value']
        self.payUrl = rjson['payUrl']

    def __repr__(self):
        return f'<Bill amount={self.amount}, status={self.status}>'


class Qiwi:
    def __init__(self, secret_key: str):
        self.SECRET_KEY = secret_key
        self.headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {self.SECRET_KEY}'
        }

    def new(self, amount: str, comment: str = None, exp_dt: str | timedelta = '15m'):
        amount = self._format_amount(amount=amount)
        bill_id = str(uuid.uuid4())
        url = f'https://api.qiwi.com/partner/bill/v1/bills/{bill_id}'

        data = {
            'amount': {
                'currency': 'RUB',
                'value': f'{amount}'
            },
            "expirationDateTime": self._create_time(exp_dt),
        }

        if comment is not None:
            data['comment'] = comment

        resp = requests.put(url=url, json=data, headers=self.headers)

        return Bill(resp)

    def status(self, bill: Bill):
        return self.check_id(bill.bill_id)

    def check_id(self, pay_id: str):
        url = f'https://api.qiwi.com/partner/bill/v1/bills/{pay_id}'
        rjson = requests.get(url=url, headers=self.headers).json()
        try:
            return rjson['status']['value']
        except KeyError:
            raise ConnectionError(rjson)

    def _format_amount(self, amount: int | float | str):
        if isinstance(amount, float):
            return str(round(amount, 2)).ljust(len(str(round(amount))) + 3, '0')
        elif isinstance(amount, int):
            return str(amount) + '.00'
        elif isinstance(amount, str):
            return self._format_amount(float(amount))
        else:
            raise ValueError(f'amount must be int/float/str, not {type(amount).__name__}')

    @staticmethod
    def _create_time(time: str | timedelta):
        if isinstance(time, str):
            dtargs = {
                'days': 0,
                'hours': 0,
                'minutes': 0,
                'seconds': 0
            }
            times = time.split(':')
            for i in times:
                code = i[-1]
                tm = i[:-1]
                if code == 'd':
                    dtargs['days'] += float(tm)
                elif code == 'h':
                    dtargs['hours'] += float(tm)
                elif code == 'm':
                    dtargs['minutes'] += float(tm)
                elif code == 's':
                    dtargs['seconds'] += float(tm)
            return datetime.isoformat(datetime.now(pytz.timezone('Europe/Moscow')) +
                                      timedelta(**dtargs)).split('.')[0] + '+03:00'
        elif isinstance(time, timedelta):
            return datetime.isoformat(datetime.now(pytz.timezone('Europe/Moscow')) +
                                      time).split('.')[0] + '+03:00'
        else:
            raise ValueError('time must be str or timedelta')
