# Visa Gift Card
import re

class VisaGiftCard:
    """A Visa Gift Card

    Input arguments:
    cardNumber -- 16-digits card number
    expirationMonth -- 2-digit expiration month
    expirationYear -- 2-digit expiration year
    cvv -- 3-digit security code
    postal -- 5-digit zip code
    initBalance -- initial load value
    currBalance -- current remaining value
    transactions -- list of transactions

    """

    def __init__(self, cardNumber, expirationMonth, expirationYear, cvv, **kwargs):
        self.cardNumber = cardNumber
        self.expirationMonth = expirationMonth
        self.expirationYear = expirationYear
        self.cvv = cvv
        self.postal = kwargs.get('postal', '00000');
        self.initBalance = kwargs.get('initBalance', 0)
        self.currBalance = kwargs.get('currBalance', 0)
        self.transactions = kwargs.get('transactions', list());

    @staticmethod
    def parse(msg):
        """Given the response message, parse it and return a VisaGiftCard object."""

    @staticmethod
    def parseLastFour(msg):
        """Given the response message, extract the last four digits of the card.

        Example message:
            ...
            <div class="data-box">
                <div class="name">Card Ending</div>
                <div class="value">7117</div>
            </div>
            ...
        """
        pattern = ("<div class=\"data-box\">[\s]*"
                   "<div class=\"name\">Card Ending</div>[\s]*"
                   "<div class=\"value\">(\d\d\d\d)</div>[\s]*"
                   "</div>")
        match = re.findall(pattern, msg)

        if len(match) == 1:
            return match[0]

        return 'Error'

    @staticmethod
    def parseInitBalance(msg):
        """Given the response message, extract the initial balance of the card.

        Example message:
            ...
            <div class="data-box">
                <div class="name">Available Balance</div>
                <div class="value">$50.00</div>
            </div>
            ...
        """
        pattern = ("<div class=\"data-box\">[\s]*"
                   "<div class=\"name\">Initial Balance</div>[\s]*"
                   "<div class=\"value\">\$(\d+.\d\d)</div>[\s]*"
                   "</div>")
        match = re.findall(pattern, msg)

        if len(match) == 1:
            return match[0]

        return 'Error'

    @staticmethod
    def parseCurrBalance(msg):
        """Given the response message, extract the current balance of the card.

        Example message:
            ...
            <div class="data-box">
                <div class="name">Available Balance</div>
                <div class="value">$50.00</div>
            </div>
            ...
        """
        pattern = ("<div class=\"data-box\">[\s]*"
                   "<div class=\"name\">Available Balance</div>[\s]*"
                   "<div class=\"value\">\$(\d+.\d\d)</div>[\s]*"
                   "</div>")
        match = re.findall(pattern, msg)

        if len(match) == 1:
            return match[0]

        return 'Error'

    @staticmethod
    def parseFiveBackAmount(msg):
        """Given the response message, extract the five back amount on the card.

        There could be multiple transactions so we should iterate all of them and
        sum up the amounts.

        Example message:
            ...
            <div class="col-xs-5ths transaction-desc">
                INTELISPEND - EGIFT -
            </div>
            <div class="col-xs-5ths transaction-amount">
                $25.00
            </div>
            ...
        """
        pattern = ("<div class=\"col-xs-5ths transaction-desc\">[\s]*"
                   "INTELISPEND - EGIFT[ -]*[\s]*"
                   "</div>[\s]*"
                   "<div class=\"col-xs-5ths transaction-amount\">[\s]*"
                   "\$(\d+.\d\d)[\s]*"
                   "</div>")
        matches = re.findall(pattern, msg)

        if len(matches) == 0:
            return 'N/A'

        cashback = 0
        for match in matches:
            cashback += float(match)

        return '{0:.2f}'.format(cashback)

    @staticmethod
    def parseOverrideAmount(msg):
        """Given the response message, extract the override amount, the amount
        that overrides by customer service, on the card.

        There could be multiple transactions so we should iterate all of them and
        sum up the amounts.

        Example message:
            ...
            <div class="col-xs-5ths transaction-desc">

            </div>
            <div class="col-xs-5ths transaction-amount">
                $25.00
            </div>
            ...
        """
        pattern = ("<div class=\"col-xs-5ths transaction-desc\">[\s]*"
                   "</div>[\s]*"
                   "<div class=\"col-xs-5ths transaction-amount\">[\s]*"
                   "\$(\d+.\d\d)[\s]*"
                   "</div>")
        matches = re.findall(pattern, msg)

        if len(matches) == 0:
            return 'N/A'

        override = 0
        for match in matches:
            override += float(match)

        return '{0:.2f}'.format(override)
