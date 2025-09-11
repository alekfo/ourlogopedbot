from peewee import IntegrityError, DoesNotExist
import telebot
from telebot import TeleBot
from telebot.types import Message, BotCommand, ReplyKeyboardRemove
from config import admin_id
from DATABASE.peewee_config import Client, Week, Lesson
from states import reg_states_client, reg_states_admin
from keyboards.main_keyboards import (
    start_registration,
    go_to_menu,
    get_contact,
    main_clients_commands,
    main_admin_commands,
    schedule_menu)



def reg_start_handlers(bot: TeleBot):

#=====БЛОК ОБРАБОТКИ ПЕРВОГО СООБЩЕНИЯ=======
    @bot.message_handler(state=None, func=lambda message: True)
    def first_message(message: Message):
        try:
            client = Client.get(Client.clients_id == message.from_user.id)
            bot.send_message(message.chat.id,
                             f'Рад снова видеть Вас, {client.clients_name}!👋\n'
                                              f'Для перехода в меню нажми на кнопку ниже',
                             reply_markup=go_to_menu()
                             )
            bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)
        except DoesNotExist:
            if message.from_user.id != admin_id:
                bot.send_message(message.chat.id,
                                 'Добро пожаловать в чат-бот центра "ЛОГОПЕДиЯ"!🦄👨‍👩‍👧‍👦\n'
                                                  'Чтобы продолжить - пройдите регистрацию по кнопке ниже',
                                 reply_markup=start_registration())
                bot.set_state(message.from_user.id, reg_states_client.start_registration, message.chat.id)
            else:
                bot.send_message(message.chat.id,
                                 'Вы являетесь администратором🥷 чата, нажмите на кнопку ниже для прохода в меню',
                                 reply_markup=go_to_menu())
                bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)


