#!/usr/bin/env python

import os.path
import csv
import configparser
from utils import VisaGiftCard

configFileName = 'config.ini'
sampleConfigFileName = 'config.sample.ini'

csvFileName = 'registration.csv'
sampleCsvFileName = 'cards.sample.csv'

configSection = 'Contact Information'

# Dictionary for JSON key => Config file key
configDict = {
    'EmailAddress': 'Email',
    'FirstName': 'FirstName',
    'Surname': 'LastName',
    'StreetAddress1': 'StreetAddress1',
    'StreetAddress2': 'StreetAddress2',
    'Town': 'City',
    'State': 'State',
    'PostalCode': 'PostalCode',
    'TeleNum': 'PhoneNumber'
}

requiredField = ['FirstName', 'Surname', 'StreetAddress1', 'Town', 'State', 'PostalCode', 'TeleNum']

if __name__ == "__main__":
    # execute only if run as a script
    if not os.path.exists(configFileName):
        print '"{}" is not found.\nPlease make a copy from "{}"'.format(configFileName, sampleConfigFileName)
        exit()

    config = configparser.ConfigParser()
    config.read(configFileName)

    contactInfo = {}
    for postKey, configKey in configDict.iteritems():
        postValue = config.get(configSection, configKey) if config.has_option(configSection, configKey) else None
        if requiredField.__contains__(postKey) and (postValue is None or postValue == ''):
            print "'{}' is missing".format(postKey)
            exit()
        contactInfo[postKey] = postValue

    try:
        f = open(csvFileName, 'r')
    except (OSError, IOError) as error:
        print '"{}" is not found.\nPlease make a copy from "{}"'.format(csvFileName, sampleCsvFileName)
        exit()


    titles = ['Last 4', 'Registered']
    separator = '  '
    header = separator.join(titles)
    print header
    print '=' * len(header)

    for row in csv.reader(f):
        if row[0] == 'Card Number': # CSV Header
            continue
        vgc = VisaGiftCard.fromRow(row)
        if vgc.valid:
            success = vgc.registerCard(contactInfo)
            print '{:>6}  {:>10}'.format(vgc.lastFour, 'Yes' if success else 'No')
    