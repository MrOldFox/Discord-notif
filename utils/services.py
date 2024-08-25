import requests

from main import TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN


# Функция для отправки сообщения в Telegram
def send_telegram_message(message, topic):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'message_thread_id': topic,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True,
    }
    requests.post(url, data=data)