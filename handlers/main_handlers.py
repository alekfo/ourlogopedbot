from peewee import IntegrityError
import telebot
from telebot import TeleBot
from telebot.types import Message, BotCommand
from DATABASE.peewee_config import Client, Schedule, create_models
from states import reg_states_client, reg_states_admin

def reg_handlers(bot: TeleBot):
    commands = [
        BotCommand("start", "Запустить бота"),
        BotCommand("help", "Помощь и команды"),
        BotCommand("history", "Посмотреть историю запросов")
    ]
    bot.set_my_commands(commands)
    # @bot.message_handler(state=None, func=lambda message: True)
    # def first_step(message: Message):
    #     try:
    #         client = Client.get(Client.clients_id == message.from_user.id)
    #     except Client.DoesNotExist:
    #
    #     bot.send_message(message.chat.id, 'Чтобы начать — введите /help', reply_markup=first_step_markup())


