# Timetable-Provider
Provide timetables with users via LINE Messaging API

## Requirment
- Python3
- Django
- [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
- PostgreSQL
- [LINE Messaging API](https://developers.line.biz/ja/docs/messaging-api/)
  - LINE Account
  - ACCESS_TOKEN
  - CHANNE_SECRET

## Installation
1. Clone this repository
2. Deploy this app on your server

## Usage 
1. Get ACCESS_TOKEN and CHANNEL_SECRET from [LINE Developpers](https://developers.line.biz/ja/)
2. Put your CHANNEL_TOKEN and CHANNEL_SECRET in **bot/view.py** or config
```py
line_bot_api = LineBotApi(os.environ['YOUR_CHANNEL_ACCESS_TOKEN'])
parser = WebhookParser(os.environ['YOUR_CHANNEL_SECRET'])
```
3. Put your Database information in **mysite/settings.py** or config
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DATABASE_URL'],
        'PORT': os.environ['DB_PORT'] ,
    }
}
```