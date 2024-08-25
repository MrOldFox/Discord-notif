import discord
import os
import logging
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
import aiohttp

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                    handlers=[logging.FileHandler('bot.log', encoding='utf-8'),
                              logging.StreamHandler()])

# Логгер бота
bot_logger = logging.getLogger('bot')

# Загрузка переменных из .env файла
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_TOPIC = os.getenv('TELEGRAM_TOPIC')
DISCORD_LINK = os.getenv('DISCORD_LINK')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Включаем необходимые намерения
intents = discord.Intents.default()
intents.message_content = True  # Для обработки содержимого сообщений
intents.members = True  # Для обработки событий, связанных с членами сервера

# Создаем класс для бота
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)  # Передаем настроенные намерения
        self.initial_extensions = [
            'cogs.general',  # Модуль с командами
            'cogs.events', # Модуль с ивентами
        ]
        self.session = None

        # Переменные для передачи в cogs
        self.logger = bot_logger
        self.discord_link = DISCORD_LINK
        self.telegram_topic = TELEGRAM_TOPIC

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()

        # Асинхронная загрузка расширений
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        # Запуск фоновой задачи
        self.background_task.start()

    async def close(self):
        if self.session:
            await self.session.close()
        await super().close()

    @tasks.loop(minutes=5)
    async def background_task(self):
        self.logger.info("Выполняется фоновая задача...")

    async def on_ready(self):
        self.logger.info(f'Бот {self.user} готов к работе!')


async def main():
    bot = MyBot()

    async with bot:
        await bot.start(DISCORD_TOKEN)


if __name__ == '__main__':
    asyncio.run(main())