import discord
import requests
import os
from dotenv import load_dotenv
import json

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
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

# Проверка наличия нужных ролей
def has_required_role(member):
    required_roles = ['Бронзовый', 'Серебряный', 'Золотой', 'Платиновый']
    return any(role.name in required_roles for role in member.roles)

# Формирование JSON файла с участниками
def save_participant_to_json(member):
    participant_data = {
        'discord_id': member.id,
        'discord_username': member.name,
        'roles': [role.name for role in member.roles]
    }

    file_path = 'participants.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
    else:
        data = []

    data.append(participant_data)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Обработчик команды /join
@client.event
async def on_message(message):
    if message.content == '/join':
        member = message.author

        if has_required_role(member):
            save_participant_to_json(member)
            await message.channel.send(f'{member.name}, вы успешно зарегистрированы для участия в аукционе!')
        else:
            await message.channel.send(
                f'{member.name}, вы не указали свой логин Discord на портале [linkrt.ru](https://linkrt.ru/change-profile/) '
                f'в личном профиле. Пожалуйста, добавьте его, чтобы участвовать в аукционе.'
            )

# Обработчик события присоединения нового пользователя
@client.event
async def on_member_join(member):
    message = (f"🎮 К серверу Discord присоединился новый участник\n\n"
                f"Участник: {member.name}\n\n"
                f"[Присоединиться к нашему Discord]({DISCORD_LINK})")
    send_telegram_message(message, TELEGRAM_TOPIC)

# Запуск бота
client.run(DISCORD_TOKEN)