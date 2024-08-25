# cogs/events.py
import discord
from discord.ext import commands
from utils.services import send_telegram_message


class Events(commands.Cog):
    """
    Класс для обработки различных событий, происходящих на сервере Discord.
    """

    def __init__(self, bot):
        """
        Инициализация класса Events.

        Параметры:
        bot : commands.Bot
            Экземпляр бота Discord.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Обработчик события on_member_join.

        Эта функция вызывается автоматически, когда новый участник присоединяется к серверу Discord.
        Отправляет уведомление в Telegram о новом участнике.

        Параметры:
        member : discord.Member
            Объект участника, который присоединился к серверу.
        """
        # Формируем сообщение с информацией о новом участнике
        message = (f"🎮 К серверу Discord присоединился новый участник\n\n"
                   f"Участник: {member.name}\n\n"
                   f"[Присоединиться к нашему Discord]({self.bot.discord_link})")

        # Отправляем сообщение в Telegram через функцию send_telegram_message
        send_telegram_message(message, self.bot.telegram_topic)


# Функция для добавления Cog к боту
async def setup(bot):
    await bot.add_cog(Events(bot))
