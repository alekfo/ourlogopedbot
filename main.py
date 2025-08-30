import telebot
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
from config import BOT_TOKEN
from handlers.main_handlers import reg_handlers

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

    bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    reg_handlers(bot)
    bot.infinity_polling()

if __name__ == '__main__':
    main()