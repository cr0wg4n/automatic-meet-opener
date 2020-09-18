# Automatic Meet Opener
This script helps you remember meets, its only compatible with Google Meet.

## We learn about
* Schedulers in python
* Proccess in python
* Google calendar API
* Times and dates

## API 

[Google Calendar Api](https://developers.google.com/calendar/quickstart/python) for developers.

## Requirements


## Execution

```bash
pip3 install -r requirements.txt
python3 main.py
```

Alternativement you can customize the script: update times, time zones, open meet a few minutes before and of course, your email.

```python
UPDATE_TIME = 120 # minutes
MINUTES_BEFORE = 2
EMAIL = ['example@gmail.com'] # yes, your email in array, maybe I will make some features more later
TIMEZONE = 'America/La_Paz' # check it out, https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
```
