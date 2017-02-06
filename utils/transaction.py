class Transaction(object):
    """Transaction

    Attributes
    ----------
    * dateStr(str)
    * typeStr(str)
    * description(str)
    * amount(float)

    """
    # Transaction Type Enum
    TypeRegular, TypeCashback, TypeOverride = range(0, 3)
    TypeName = ['Regular', 'Cashback', 'Override']

    def __init__(self, dateStr=None, typeStr=None, description='', amount=0.0):
        self.dateStr = dateStr
        self.typeStr = typeStr
        self.description = description
        self.amount = amount

    def __str__(self):
        return 'Transaction date:{} type:{} amount:${:,.2f} description:{}'.format(self.dateStr, self.TypeName[self.transactionType], self.amount, self.description)

    @property
    def transactionType(self):
        if self.amount > 0 and self.description.startswith('INTELISPEND - EGIFT'):
            return self.TypeCashback
        elif self.amount > 0 and self.typeStr is None:
            return self.TypeOverride
        else:
            return self.TypeRegular
