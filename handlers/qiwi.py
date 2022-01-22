import datetime
import uuid
from dataclasses import dataclass

import pyqiwi

from data import config

wallet = pyqiwi.Wallet(token=config.QIWI, number=config.QIWI_NUMBER)


class NoPaymentFound(Exception):
    pass


class NotEnoughMoney(Exception):
    pass


@dataclass
class Payment:
    amount: int
    payment_key: str = None

    def create(self):
        self.payment_key = str(uuid.uuid4())

    def check_payment(self):
        transactions = wallet.history(start_date=datetime.datetime.now() - datetime.timedelta(days=2)).get(
            'transactions')
        for transaction in transactions:
            if transaction.comment:
                if str(self.payment_key) in transaction.comment:
                    if float(transaction.total.amount) >= float(self.amount):
                        return True
                    else:
                        raise NotEnoughMoney
        else:
            raise NoPaymentFound

    @property
    def invoice(self):
        payment_link = f'https://oplata.qiwi.com/create?publicKey={config.QIWI_PUB}&amount={self.amount}&comment={self.payment_key}'
        return payment_link