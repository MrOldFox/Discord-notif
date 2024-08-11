import discord
import requests
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_TOPIC = os.getenv('TELEGRAM_TOPIC')
DISCORD_LINK = os.getenv('DISCORD_LINK')

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

# Создание экземпляра клиента Discord
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Обработчик события присоединения нового пользователя
@client.event
async def on_member_join(member):
    message = (f"🎮 К серверу Discord присоединился новый участник\n\n"
                f"Участник: {member.name}\n\n"
                f"[Присоединиться к нашему Discord]({DISCORD_LINK})")
    send_telegram_message(message, TELEGRAM_TOPIC)

# Запуск бота
client.run(DISCORD_TOKEN)
