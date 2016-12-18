# Balance Checker
Check the remaining balance of your Visa gift cards issued by Blackhawk Network California, Inc. with this Python script.

## Dependencies
This script depends on Python module `re`(RegEx), `csv`, and `requests`. The first two modules are included in Python so you will need to install `requests` module if necessary. Use the following command to install `requests`.

### Windows Systems
You have two choices: 1) refer to https://www.python.org/downloads/windows/ and install Python for Windows, or 2) install Cygwin from https://cygwin.com/ and then install Python for Cygwin. After having Python and `pip` installed, run the following command to install the dependencies.
```
$ pip install -r requirements.txt
```

### Ubuntu/Debian/Linux Mint
Install `pythin-pip` package with
```
$ sudo apt-get -y install python-pip
```
and then run the following command to install the dependencies.
```
$ sudo pip install -r requirements.txt
```

## Card Information
Card information is stored in CSV format in `cards.csv` file with only one card in each line, `Card Number`, `Month`, `Year` , `CVV`, `Zip Code`, and `Note` are separated with commas. Edit `cards.csv` to import your cards. If you have registered your card, you need to provide the zip code; otherwise you can leave it blank.

## Check Card Balance
Use the following command to run the script:
```
$ ./balchecker.py
```
