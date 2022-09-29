from datetime import datetime, timedelta
import requests
import pytz
import uuid

class Bill:
    def __init__(self, resp):
        rjson = resp.json()
        self.bill_id = rjson['billId']
        self.expDT = rjson['expirationDateTime']
        self.amount = rjson['amount']['value']
        self.status = rjson['status']['value']
        self.payUrl = rjson['payUrl']
    
    
    def __repr__(self):
        return f'<Bill amount={self.amount}, status={self.status}>'



class Qiwi:
    def __init__(self, secret_key):
        self.SECRET_KEY = secret_key


    def create_bill(self, amount, comment=None, expDT='15m'):
        amount = self._format_amount(amount=amount)
        bill_id = str(uuid.uuid4())
        url = f'https://api.qiwi.com/partner/bill/v1/bills/{bill_id}'
        headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {self.SECRET_KEY}'
        }

        data = {
            'amount':{
                'currency': 'RUB',
                'value': f'{amount}'
            },
            "expirationDateTime": self._create_time(expDT),
        }
        
        if not comment == None:
            data['comment'] = comment
        
        resp = requests.put(url=url, json=data, headers=headers)
        
        return Bill(resp)
    
    def bill_status(self, bill: Bill):
        return self.check_pay_id(bill.bill_id)


    def check_pay_id(self, pay_id):
        url = f'https://api.qiwi.com/partner/bill/v1/bills/{pay_id}'
        headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {self.SECRET_KEY}'
        }
        rjson = requests.get(url=url, headers=headers).json()
        return rjson['status']['value']


    def _format_amount(self, amount):
        if isinstance(amount, float):
            return str(round(amount, 2)).ljust(len(str(round(amount))) + 3, '0')
        elif isinstance(amount, int):
            return str(amount) + '.00'
        elif isinstance(amount, str):
            return self._format_amount(float(amount))


    def _create_time(self, s: str):
        dtargs = {
        'days'   :0,
        'hours'  :0,
        'minutes':0,
        'seconds':0
        }
        times = s.split(':')
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
        return datetime.isoformat(datetime.now(pytz.timezone('Europe/Moscow')) + timedelta(**dtargs)).split('.')[0] + '+03:00'

