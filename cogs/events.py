# cogs/events.py
import discord
from discord.ext import commands
from utils.services import send_telegram_message

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # При подключении нового участника отправляем сообщение в Telegram
        message = (f"🎮 К серверу Discord присоединился новый участник\n\n"
                   f"Участник: {member.name}\n\n"
                   f"[Присоединиться к нашему Discord]({self.bot.discord_link})")
        send_telegram_message(message, self.bot.telegram_topic)
        # Можно добавить уведомление и в сам Discord канал
        channel = discord.utils.get(member.guild.text_channels, name="general")  # Замените на ваш канал
        print(1)
        if channel:
            await channel.send(f"Добро пожаловать на сервер, {member.mention}!")

# Функция для добавления Cog к боту
async def setup(bot):
    await bot.add_cog(Events(bot))
