import os

ENVIRONMENT_DEFAULT_VARIABLES = {
    "DEBUG": "True",
    "SECRET_KEY": "Kji327a09a)*hjk2H*@9AS#@13ew!9",
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': '465',
    'MAIL_USERNAME': 'nixonsparrow@gmail.com',
    'MAIL_PASSWORD': 'imyegsfnwappguin',
    'MAIL_USE_TLS': 'False',
    'MAIL_USE_SSL': 'True',
}

for k, v in ENVIRONMENT_DEFAULT_VARIABLES.items():
    os.environ.setdefault(k, v)
