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


# Создание экземпляра клиента Discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)


# Проверка наличия нужных ролей
def has_required_role(member):
    required_roles = ['Бронзовый', 'Серебряный', 'Золотой', 'Платиновый']
    return any(role.name in required_roles for role in member.roles)


# Регистрация в мероприятии
def manage_participants(member=None, action='load', file_path='participants_dota2.json'):
    """
    Универсальная функция для управления участниками мероприятий.
    Поддерживает следующие действия:
    - 'load': возвращает список всех участников
    - 'add': добавляет нового участника в список и сохраняет его
    - 'check': проверяет, зарегистрирован ли участник
    """
    if action == 'load':
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    elif action == 'add' and member:
        participants = manage_participants(action='load', file_path=file_path)
        participant_data = {
            'discord_id': member.id,
            'discord_username': member.name,
            'roles': [role.name for role in member.roles]
        }
        participants.append(participant_data)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(participants, f, ensure_ascii=False, indent=4)

    elif action == 'check' and member:
        participants = manage_participants(action='load', file_path=file_path)
        return any(participant['discord_id'] == member.id for participant in participants)

    return None


# Обработчик команды /join
@client.event
async def on_message(message):
    if message.content == '/join':
        member = message.author

        # Проверка на уже существующую регистрацию
        if manage_participants(member, action='check'):
            await message.channel.send(f'{member.name}, вы уже зарегистрированы для участия в игре по Dota 2!')
            return

        # Проверка на наличие нужной роли
        if has_required_role(member):
            # Добавление участника в файл
            manage_participants(member, action='add')
            await message.channel.send(f'{member.name}, вы успешно зарегистрированы для участия в игре по Dota 2!')

            # Отправка сообщения в Telegram
            message = (f"🎮 К мини-турниру Dota 2 присоединился новый участник\n\n"
                       f"Участник: {member.name}\n\n"
                       f"[Присоединиться к нашему Discord]({DISCORD_LINK})")
            send_telegram_message(message, TELEGRAM_TOPIC)
        else:
            await message.channel.send(
                f'Вы не указали свой логин Discord ({member.name}) на портале '
                f'[linkrt.ru](https://linkrt.ru/change-profile/) в личном профиле. '
                f'Либо не прошло обновление данных с сервера, если в '
                f'течении часа ничего не изменится обратитесь к @Админ'
            )


# Обработчик события присоединения нового пользователя
@client.event
async def on_member_join(member):
    message = (f"🎮 К серверу Discord присоединился новый участник\n\n"
                f"Участник: {member.name}\n\n"
                f"[Присоединиться к нашему Discord]({DISCORD_LINK})")
    send_telegram_message(message, TELEGRAM_TOPIC)


# Обработчик команды /nick
@client.event
async def on_message(message):
    if message.content == '/name':
        member = message.author
        discord_username = member.name

        # Отправляем сообщение и сохраняем его для последующего удаления
        bot_message = await message.channel.send(
            f"Ваш уникальный ник в Discord: **{discord_username}**\n\n"
            f"Необходимо указать этот никнейм в вашем личном "
            f"профиле на сайте [linkrt.ru](https://linkrt.ru/change-profile/), "
            f"чтобы интегрировать вашу учетную запись и получить доступ к наградам и возможностям нашего сообщества."
        )

        # Удаляем сообщение пользователя через 5 минут (300 секунд)
        await message.delete(delay=300)
        # Удаляем сообщение бота через 5 минут (300 секунд)
        await bot_message.delete(delay=300)


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

# Запуск бота
client.run(DISCORD_TOKEN)