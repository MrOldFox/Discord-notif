import os
import json
from main import bot_logger


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
    try:
        if action == 'load':
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    bot_logger.info('Загружаем список участников из файла.')
                    return json.load(f)
            bot_logger.info('Файл с участниками не найден. Возвращаем пустой список.')
            return []

        elif action == 'add' and member:
            bot_logger.info(f'Добавляем участника: {member.name} (ID: {member.id}).')
            participants = manage_participants(action='load', file_path=file_path)
            participant_data = {
                'discord_id': member.id,
                'discord_username': member.name,
                'roles': [role.name for role in member.roles]
            }
            participants.append(participant_data)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(participants, f, ensure_ascii=False, indent=4)
            bot_logger.info(f'Участник {member.name} успешно добавлен и данные сохранены в файл.')

        elif action == 'check' and member:
            bot_logger.info(f'Проверяем регистрацию участника: {member.name} (ID: {member.id}).')
            participants = manage_participants(action='load', file_path=file_path)
            registered = any(participant['discord_id'] == member.id for participant in participants)
            if registered:
                bot_logger.info(f'Участник {member.name} уже зарегистрирован.')
            else:
                bot_logger.info(f'Участник {member.name} не зарегистрирован.')
            return registered

    except Exception as e:
        bot_logger.exception(f'Ошибка в процессе управления участниками: {str(e)}')
        raise e