import telebot
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
from config import BOT_TOKEN
import threading
from config import admin_id

from handlers.start_handlers import reg_start_handlers
from handlers.menu_handlers import reg_menu_handlers
from handlers.clients_handlers import reg_clients_handlers
from handlers.registration_handlers import reg_registration_handlers
from handlers.schedule.schedule_handlers import reg_schedule_handlers
from handlers.schedule.menage_schedule import reg_menage_schedule_handlers
from handlers.downloads_handlers import reg_downloads_handlers
from handlers.mass_mailing_handler import reg_mass_mailing_handler
from handlers.info_for_admin_handler import reg_info_about_clients
from handlers.menage_clients import reg_menage_clients

from DATABASE.peewee_config import create_models
from utils.notifications import check_upcoming_lessons

state_storage = StateMemoryStorage()

def main():
    """
    Основная функция для запуска бесконечного цикла взаимодействия с API
    сервера телеграма.
    Переменной bot присваивается объект класса TeleBot.
    Переменная bot регистрирует все возможные сценарии полученных сообщений
    в функции reg_handlers.
    С помощью bot.infinity_polling() запускается бесконечный цикл опроса API
    телеграма
    """

    create_models()
    bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    reg_menu_handlers(bot)
    reg_info_about_clients(bot)
    reg_schedule_handlers(bot)
    reg_menage_schedule_handlers(bot)
    reg_menage_clients(bot)
    reg_downloads_handlers(bot)
    reg_mass_mailing_handler(bot)

    reg_clients_handlers(bot)
    reg_registration_handlers(bot)
    reg_start_handlers(bot)

    # Запускаем поток для проверки уведомлений
    notification_thread = threading.Thread(
        target=check_upcoming_lessons,
        args=(bot,),
        daemon=True  # Поток завершится при завершении основного потока
    )
    notification_thread.start()
    bot.send_message(admin_id,
                     f'Поток уведомлений запущен')

    bot.infinity_polling()

if __name__ == '__main__':
    main()