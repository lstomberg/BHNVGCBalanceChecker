#!/usr/bin/env python

import csv
from utils import VisaGiftCard

fileName = 'cards.csv'
sampleFileName = 'cards.sample.csv'

def newCard(row):
    if len(row) != 6:
        return None
    cardNumber, month, year, cvv, postal, note = row
    return VisaGiftCard(cardNumber, month, year, cvv, postal)

if __name__ == "__main__":
    # execute only if run as a script
    try:
        f = open(fileName, 'r')
    except (OSError, IOError) as error:
        print '"{}" is not found.\nPlease make a copy from "{}"'.format(fileName, sampleFileName)
        exit()

    titles = ['Last 4', 'Available', 'Initial', 'Cashback', 'Override']
    separator = '  '
    header = separator.join(titles)
    print header
    print '=' * len(header)

    for row in csv.reader(f):
        if row[0] == 'Card Number': # CSV Header
            continue
        vgc = newCard(row)
        vgc.getBalanceAndTransactions()
        formatStr = lambda x: '{:>%i}' % len(x) # Take a string and return right align format '{:>x}' where x is the length of the input
        formatFloat = lambda x: '{:>%i.2f}' % len(x)
        if vgc.valid:
            indentFormat = formatStr(titles[0]) + separator + separator.join(map(formatFloat, titles[1:])) # '{:>6}  {:>9}  {:>7}  {:>8}  {:>8}'
            print indentFormat.format(vgc.lastFour, vgc.availableBalance, vgc.initialBalance, vgc.cashback, vgc.override)
        else:
            indentFormat = formatStr(titles[0]) + separator + formatStr(separator.join(titles[1:]))
            print indentFormat.format(vgc.lastFour, 'ERROR: ' + vgc.errorMessage)

    f.close()
