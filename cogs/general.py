# cogs/general.py
from discord.ext import commands
import asyncio  # Для работы с задержкой
from utils.helpers import manage_participants, has_required_role
from utils.services import send_telegram_message


class Greetings(commands.Cog):
    """
    Класс для реализации команд приветствия и регистрации пользователей на сервере Discord.
    Команды позволяют пользователям взаимодействовать с ботом для получения важной информации.
    """

    def __init__(self, bot, logger, discord_link, telegram_topic):
        """
        Инициализация класса Greetings.

        Параметры:
        bot : commands.Bot
            Экземпляр бота Discord.
        logger : logging.Logger
            Логгер для записи информации о действиях и ошибках.
        discord_link : str
            Ссылка на сервер Discord для использования в сообщениях.
        telegram_topic : str
            Идентификатор темы для отправки сообщений в Telegram.
        """
        self.bot = bot
        self.logger = logger
        self.discord_link = discord_link
        self.telegram_topic = telegram_topic

    @commands.command(name='name')
    async def name(self, ctx):
        """
        Команда !name.

        Отправляет пользователю сообщение с его уникальным никнеймом Discord
        и инструкцией по обновлению профиля на сайте сообщества.

        Параметры:
        ctx : commands.Context
            Контекст команды, который предоставляет доступ к информации о сообщении и авторе.
        """
        member = ctx.author  # Получаем объект участника, который вызвал команду
        discord_username = member.name  # Извлекаем имя пользователя Discord

        # Отправляем сообщение пользователю с его никнеймом и инструкцией по интеграции аккаунта
        bot_message = await ctx.send(
            f"Ваш уникальный ник в Discord: **{discord_username}**\n\n"
            f"Необходимо указать этот никнейм в вашем личном профиле на сайте "
            f"[linkrt.ru](https://linkrt.ru/change-profile/), чтобы интегрировать вашу учетную запись и "
            f"получить доступ к наградам и возможностям нашего сообщества."
        )

        # Ждем 300 секунд (5 минут), чтобы пользователь успел прочитать сообщение
        await asyncio.sleep(300)
        # Удаляем сообщение пользователя и бота по истечении времени
        await ctx.message.delete()
        await bot_message.delete()

    @commands.command(name='join')
    async def join(self, ctx):
        """
        Команда !join.

        Регистрирует пользователя для участия в мини-турнире по Dota 2, если он не зарегистрирован.
        Также отправляет уведомление в Telegram о новом участнике.

        Параметры:
        ctx : commands.Context
            Контекст команды, который предоставляет доступ к информации о сообщении и авторе.
        """
        member = ctx.author  # Получаем объект участника, который вызвал команду
        self.logger.info(f'Получена команда /join от пользователя {member.name} (ID: {member.id}).')

        try:
            # Проверка, зарегистрирован ли пользователь
            if manage_participants(member, action='check'):
                await ctx.send(f'{member.name}, вы уже зарегистрированы для участия в игре по Dota 2!')
                self.logger.info(f'Пользователь {member.name} уже зарегистрирован.')
                return

            # Проверка наличия нужной роли для регистрации
            if has_required_role(member):
                # Добавляем пользователя в список участников
                manage_participants(member, action='add')
                await ctx.send(f'{member.name}, вы успешно зарегистрированы для участия в игре по Dota 2!')
                self.logger.info(f'Пользователь {member.name} успешно зарегистрирован.')

                # Отправляем уведомление о новом участнике в Telegram
                telegram_message = (f"🎮 К мини-турниру Dota 2 присоединился новый участник\n\n"
                                    f"Участник: {member.name}\n\n"
                                    f"[Присоединиться к нашему Discord]({self.discord_link})")
                send_telegram_message(telegram_message, self.telegram_topic)
                self.logger.info(f'Отправлено сообщение в Telegram о регистрации пользователя {member.name}.')
            else:
                # Если пользователь не указал свой Discord ник на портале
                await ctx.send(
                    f'Вы не указали свой логин Discord ({member.name}) на портале '
                    f'[linkrt.ru](https://linkrt.ru/change-profile/) в личном профиле. '
                    f'Либо не прошло обновление данных с сервера, если в '
                    f'течении часа ничего не изменится, обратитесь к @Админ'
                )
                self.logger.warning(f'Пользователь {member.name} не имеет нужной роли для участия.')

        except Exception as e:
            # Логируем и отправляем сообщение об ошибке пользователю в случае сбоя
            self.logger.exception(
                f'Произошла ошибка при обработке команды /join от пользователя {member.name}: {str(e)}')
            await ctx.send('Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже.')


# Функция для добавления Cog к боту
async def setup(bot):
    # Получаем необходимые переменные из бота
    logger = bot.logger
    discord_link = bot.discord_link
    telegram_topic = bot.telegram_topic

    # Создаем экземпляр класса Cog и передаем необходимые параметры
    await bot.add_cog(Greetings(bot, logger, discord_link, telegram_topic))
