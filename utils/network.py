
from HTMLParser import HTMLParser
from transaction import Transaction
import requests

DEBUG = False

class BHNRequest(object):
    """BHNRequest

    Attributes
    ----------
    *requestType(int): `BHNRequest.TypeBalance`, `BHNRequest.TypeRegister` or `BHNRequest.TypeSetPin`
    *data(dict): JSON dictionary for POST request

    """

    DOMAIN = 'https://mygift.giftcardmall.com/'
    HEADER = {'X-Requested-With': 'XMLHttpRequest', 'Referer': DOMAIN}

    # Request Type Enum
    TypeBalance, TypeRegister, TypeSetPin = range(0, 3)

    URLS = {
        TypeBalance : 'Card/_Login?returnUrl=Transactions',
        # TypeRegister : 'Account/_Profile/form-complete-reg?name=complete-reg',
        # TypeSetPin : 'Card/_SetPin/setpin-form'
    }

    def __init__(self, requestType, data):
        self.url = BHNRequest.DOMAIN + BHNRequest.URLS[requestType]
        self.data = data

    def send(self):
        """Send a POST request and return response.text"""
        response = requests.post(self.url, headers=BHNRequest.HEADER, data=self.data, verify=not DEBUG)
        return response.text

class PageParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.availableBalance = None
        self.initialBalance = None
        self.transactions = []

        self.currentTag = None
        self.currentClass = None
        self.currentName = None
        self.transaction = None

    def handle_starttag(self, tag, attrs):
        self.currentTag = tag
        self.currentClass = None
        if len(attrs) > 0:
            attrDict = dict(attrs)
            if attrDict.has_key('class'):
                self.currentClass = attrDict['class']
                if self.currentClass == 'panel-heading':
                    self.transaction = Transaction()
                elif self.currentClass == 'panel-collapse collapse':
                    # Log Transaction
                    self.transactions.append(self.transaction)
                    self.transaction = None

    def handle_data(self, data):
        content = data.strip() # Remove all white spaces and new line chars from data
        if content == '':
            return
        moneyStrToFloat = lambda x: float(x.replace('$', ''))
        if self.currentTag == 'div':
            if self.currentClass == 'name':
                self.currentName = content
            elif self.currentClass == 'value':
                if self.currentName == 'Available Balance':
                    self.availableBalance = moneyStrToFloat(content)
                elif self.currentName == 'Initial Balance':
                    self.initialBalance = moneyStrToFloat(content)
                self.currentName = None
            elif self.currentClass.startswith('col-xs-5ths transaction-'):
                key = self.currentClass.split('-')[-1]
                if key == 'type':
                    self.transaction.typeStr = content
                elif key == 'desc':
                    self.transaction.description = content
                elif key == 'amount':
                    self.transaction.amount = moneyStrToFloat(content)
        elif self.currentTag == 'span' and self.currentClass == 'glyphicon glyphicon-plus':
            self.transaction.dateStr = content
