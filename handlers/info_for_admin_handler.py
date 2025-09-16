from logging import raiseExceptions

from peewee import IntegrityError, DoesNotExist
import telebot
from datetime import datetime
import openpyxl
from io import BytesIO
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

def reg_info_about_clients(bot: TeleBot):

    # ========БЛОК ИНФОРМАЦИИ О КЛИЕНТАХ===========
    @bot.message_handler(state=reg_states_admin.in_any_block,
                         func=lambda message: 'ИНФО о клиентах' in message.text)
    def clients_info(message: Message):
        output_info = ('Вот вся информация об активных клиентах:\n\n')
        clients = Client.select()
        for i_client in clients:
            output_info += str(i_client)
        bot.send_message(message.chat.id,
                        output_info,
                        reply_markup=go_to_menu(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)

    # ========КОНЕЦ БЛОКА ИНФОРМАЦИИ О КЛИЕНТАХ===========