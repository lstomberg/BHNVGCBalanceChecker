# Visa Gift Card
import re
from transaction import Transaction
from network import BHNRequest, PageParser

class VisaGiftCard(object):
    """Visa Gift Card

    Attributes
    ----------
    * cardNumber(str): 16-digits card number
    * expMonth(str): 2-digit expiration month
    * expYear(str): 2-digit expiration year
    * cvv(str): 3-digit security code
    * postal(str): 5-digit zip code
    * valid(bool): card is valid or not
    * errorMessage(str): error message for invalid card

    Read only properties
    --------------------
    * lastFour(str)
    * cardInfo(dict)
    * initialBalance(float)
    * availableBalance(float)
    * cashback(float)
    * override(float)

    """

    def __init__(self, cardNumber, expirationMonth, expirationYear, cvv, postal):
        self.cardNumber = cardNumber
        self.expMonth = expirationMonth
        self.expYear = expirationYear
        self.cvv = cvv
        self.postal = postal
        self.errorMessage = None
        self.valid = self.validation()

        self.transactions = []
        self.reset()

    def reset(self):
        """Reset all attributes getting from network"""
        self._initialBalance = self._availableBalance = self._cashback = self._override = 0.0

    def __str__(self):
        return 'Card {} {}/{} cvv:{} {}/{}'.format(self.lastFour, self.expMonth, self.expYear, self.cvv, self.availableBalance, self.initialBalance)

    def validation(self):

        if not len(self.cardNumber) == 16:
            self.errorMessage = 'invalid card number'
            return False
        if not '4' in self.cardNumber[0]:
            self.errorMessage = 'not a VISA gift card'
            return False

        if len(self.expMonth) == 1:
            self.expMonth = '0' + self.expMonth
        if not (int(self.expMonth) > 0 and int(self.expMonth) < 13):
            self.errorMessage = 'invalid month {}'.format(self.expMonth)
            return False

        if not (int(self.expYear) > 15 and int(self.expYear) < 100):
            self.errorMessage = 'invalid year {}'.format(self.expYear)
            return False

        if not (int(self.cvv) > -1 and int(self.cvv) < 1000):
            self.errorMessage = 'invalid cvv {}'.format(self.cvv)
            return False

        self.postal = self.postal or '00000'
        if not len(self.postal) == 5:
            self.errorMessage = 'invalid postal {}'.format(self.postal)
            return False

        return True

    def getBalanceAndTransactions(self):
        """Get balace through HTTP request. Return a bool represent request successful or not"""
        if not self.valid:
            return False
        self.reset()

        responseStr = BHNRequest(BHNRequest.TypeBalance, self.cardInfo).send()
        parser = PageParser()
        parser.feed(responseStr)

        if parser.initialBalance is None or parser.availableBalance is None:
            self.valid = False
            self.errorMessage = 'card not found'
            return False

        self._initialBalance = parser.initialBalance
        self._availableBalance = parser.availableBalance
        self.transactions = parser.transactions
        for transaction in self.transactions:
            if transaction.transactionType == Transaction.TypeCashback:
                self._cashback += transaction.amount
            elif transaction.transactionType == Transaction.TypeOverride:
                self._override += transaction.amount

        self.valid = True
        self.errorMessage = None
        return True

    # Read only properties

    @property
    def lastFour(self):
        """Return last four digit of card number."""
        return self.cardNumber[-4:]

    @property
    def cardInfo(self):
        """Return JSON dictionary for POST request."""
        json = {
            'CardNumber': self.cardNumber,
            'ExpirationMonth': self.expMonth,
            'ExpirationYear': self.expYear,
            'SecurityCode': self.cvv
            }
        if self.postal != '00000':
            json['PostalCode'] = self.postal
        return json

    @property
    def initialBalance(self):
        """Return initial card balance"""
        return self._initialBalance

    @property
    def availableBalance(self):
        """Return available card balance"""
        return self._availableBalance

    @property
    def cashback(self):
        """Return available card balance"""
        return self._cashback

    @property
    def override(self):
        """Return available card balance"""
        return self._override
