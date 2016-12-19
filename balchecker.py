#!/usr/bin/env python

import csv
import re
import requests

fileName = 'cards.csv'

def getBalance(cardInfo):
    url1 = 'https://mygift.giftcardmall.com/Card/Login?returnUrl=Transactions'
    url2 = 'https://mygift.giftcardmall.com/Card/Transactions'
    headers = {'Referer': url1}
    response = requests.post(url1, data=cardInfo, allow_redirects=False)
    cookies = response.cookies
    response = requests.get(url2, headers=headers, cookies=cookies, allow_redirects=False)

    match = re.findall(r"<h6\>([a-zA-Z ]+)</h6><h5>(.+)</h5></td>", response.text)

    if len(match) == 3:
        lastFour = match[0][1]
        availableBalance = match[1][1]
        initialBalance = match[2][1]
        cashbackMatch = re.findall(r"INTELISPEND - EGIFT.+\"textRightAlign\">\$([\d.]+)", response.text)
        cashback = reduce(lambda x, y: x+float(y), cashbackMatch, 0.0) if len(cashbackMatch) > 0 else 0.0
        return {'lastFour': lastFour, 'availableBalance': availableBalance, 'initialBalance': initialBalance, 'cashback': "${0:.2f}".format(cashback)}

    return {'lastFour': '-1', 'availableBalance': '0', 'initialBalance': '0', 'cashback': '0'}

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

    return {'CardNumber': cardNumber, 'ExpirationMonth': month, 'ExpirationYear': year, 'SecurityCode': cvv2, 'PostalCode': postal, 'Note': note}

if __name__ == "__main__":
    # execute only if run as a script
    f = open(fileName, 'r')

    print '{:>13} {:>10} {:>8} {:>9}'.format('Last 4 Digits', 'Available', 'Initial', 'Cashback')
    print '==========================================='

    for row in csv.reader(f):
        cardInfo = validateCard(row)
        if cardInfo is None:
            continue

        balance = getBalance(cardInfo)
        if balance.get('lastFour') == '-1':
            print '{:>13} {:>29}'.format(cardInfo.get('CardNumber')[-4:], 'Card not found')
        else:
            print '{:>13} {:>10} {:>8} {:>9}'.format(balance.get('lastFour'), balance.get('availableBalance'), balance.get('initialBalance'), balance.get('cashback'))

    f.close()
