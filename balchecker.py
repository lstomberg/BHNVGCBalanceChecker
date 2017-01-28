#!/usr/bin/env python

import csv
import requests

from utils import cards

fileName = 'cards.csv'

def getBalance(cardInfo):
    url1 = 'https://mygift.giftcardmall.com/Card/_Login?returnUrl=Transactions'
    url2 = 'https://mygift.giftcardmall.com/Card/_CardTransactions'
    headers = {'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://mygift.giftcardmall.com/'}
    cardInfo['X-Requested-With'] = 'XMLHttpRequest'

    response = requests.post(url1, data=cardInfo, allow_redirects=False)
    cookies = response.cookies
    response = requests.get(url2, headers=headers, cookies=cookies)

    lastFour = cards.VisaGiftCard.parseLastFour(response.text)
    availableBalance = cards.VisaGiftCard.parseCurrBalance(response.text)
    initialBalance = cards.VisaGiftCard.parseInitBalance(response.text)
    cashback = cards.VisaGiftCard.parseFiveBackAmount(response.text)
    override = cards.VisaGiftCard.parseOverrideAmount(response.text)

    return {'lastFour': lastFour, 'availableBalance': availableBalance, 'initialBalance': initialBalance, 'cashback': cashback, 'csrOverride': override}

def validateCard(row):
    cardNumber = row[0]
    month = row[1]
    year = row[2]
    cvv2 = row[3]
    postal = row[4]
    note = row[5]

    if cardNumber == 'Card Number':
        return None
    if not len(cardNumber) == 16:
        print 'Error: card number {} does not have 16 digits.'.format(cardNumber)
        return None
    if not '4' in cardNumber[0]:
        print 'Error: card number {} is not a VISA gift card.'.format(cardNumber)
        return None
    if not (int(month) > 0 and int(month) < 13):
        print 'Error: card number {} has invalid month {}.'.format(cardNumber, month)
        return None
    if not (int(year) > -1 and int(year) < 100):
        print 'Error: card number {} has invalid year {}.'.format(cardNumber, year)
        return None
    if not (int(cvv2) > -1 and int(cvv2) < 1000):
        print 'Error: card number {} has invalid CVV {}.'.format(cardNumber, cvv)
        return None
    if len(month) == 1:
        month = '0' + month
    if postal == '':
        postal = '00000'

    return {'CardNumber': cardNumber, 'ExpirationMonth': month, 'ExpirationYear': year, 'SecurityCode': cvv2}

if __name__ == "__main__":
    # execute only if run as a script
    f = open(fileName, 'r')

    print '{:>6} {:>10} {:>8} {:>9} {:>9}'.format('Last 4', 'Available', 'Initial', 'Cashback', 'Override')
    print '=============================================='

    for row in csv.reader(f):
        cardInfo = validateCard(row)
        if cardInfo is None:
            continue

        balance = getBalance(cardInfo)
        if balance.get('lastFour') == '-1':
            print '{:>6} {:>29}'.format(cardInfo.get('CardNumber')[-4:], 'Card not found')
        else:
            print '{:>6} {:>10} {:>8} {:>9} {:>9}'.format(balance.get('lastFour'), balance.get('availableBalance'), balance.get('initialBalance'), balance.get('cashback'), balance.get('csrOverride'))

    f.close()
