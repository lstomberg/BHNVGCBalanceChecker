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

### Mac OSX
To make your life easier, homebrew python is recommended. See detail [here](http://docs.python-guide.org/en/latest/starting/install/osx/#install-osx).

1. Install homebrew. Skip this if your already have it.

   ```
   $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
   ```

2. Install python 2.7 from homebrew.

   ```
   $ brew install python
   ```

3. Install requests library.

   ```
   $ sudo pip install -r requirements.txt
   ```

4. Restart the terminal to clear python cache.

## Card Information
Card information should be stored in CSV format in `cards.csv` file with only one card in each line, `Card Number`, `Month`, `Year` , `CVV`, `Zip Code`, and `Note` are separated with commas. 
Run the following command to copy `cards.csv` from `cards.sample.csv`.
```
$ cp cards.sample.csv cards.csv
```
Edit `cards.csv` to import your cards. If you have registered your card, you need to provide the zip code; otherwise you can leave it blank.

## Check Card Balance
Use the following command to run the script:
```
$ ./balchecker.py
```
