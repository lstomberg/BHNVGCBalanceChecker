#!/usr/bin/env python

import os.path
import csv
import re
import configparser
from utils import VisaGiftCard

configFileName = 'config.ini'
sampleConfigFileName = 'config.sample.ini'

csvFileName = 'setpin.csv'
sampleCsvFileName = 'cards.sample.csv'

configSection = 'Default Pin'
configOption = 'PinCode'

if __name__ == "__main__":
    # execute only if run as a script
    if not os.path.exists(configFileName):
        print '"{}" is not found.\nPlease make a copy from "{}"'.format(configFileName, sampleConfigFileName)
        exit()

    config = configparser.ConfigParser()
    config.read(configFileName)
    defaultPin = config.get(configSection, configOption)

    try:
        f = open(csvFileName, 'r')
    except (OSError, IOError) as error:
        print '"{}" is not found.\nPlease make a copy from "{}"'.format(csvFileName, sampleCsvFileName)
        exit()


    titles = ['Last 4', 'Set PIN']
    separator = '  '
    header = separator.join(titles)
    print header
    print '=' * len(header)

    for row in csv.reader(f):
        if row[0] == 'Card Number': # CSV Header
            continue
        vgc = VisaGiftCard.fromRow(row)
        note = row[5] if len(row) == 6 else ''
        pin = note if re.match(r'^\d{4}$', note) else defaultPin
        if vgc.valid:
            success = vgc.setPin(pin)
            print '{:>6}  {:>7}'.format(vgc.lastFour, pin if success else 'N/A')
    