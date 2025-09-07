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


def reg_mass_mailing_handler(bot: TeleBot):
    # ========БЛОК ЗАПРОСА СООБЩЕНИЯ ДЛЯ РАССЫЛКИ===========
    @bot.message_handler(state=reg_states_admin.in_any_block,
                         func=lambda message: message.text == 'Сделать рассылку')
    def get_message(message: Message):
        bot.send_message(message.chat.id,
                        'Напишите сообщение. ПРЕДУПРЕЖДЕНИЕ: данное сообщение отправится всем зарегистрированным клиентам\n'
                        'Для отмены нажмите на кнопку "Перейти в основное меню"',
                        reply_markup=go_to_menu())
        bot.set_state(message.from_user.id, reg_states_admin.mass_mailing_state, message.chat.id)

    # ========КОНЕЦ БЛОКА ЗАПРОСА СООБЩЕНИЯ ДЛЯ РАССЫЛКИ===========


    #====БЛОК РАССЫЛКИ====
    @bot.message_handler(state=reg_states_admin.mass_mailing_state)
    def mass_mailing(message: Message):
        if message.text == 'Перейти в основное меню':
            bot.send_message(message.chat.id,
                             'Выберите действие',
                             reply_markup=main_admin_commands())
            bot.set_state(message.from_user.id, reg_states_admin.in_any_block, message.chat.id)
        else:
            clients = Client.select()
            for i_client in clients:
                bot.send_message(i_client.clients_chat_id,
                                 message.text)
            bot.send_message(message.chat.id,
                             'Сообщение отправлено всем пользователям\nПри ошибочной отправке рекомендуется обратиться к клиентам лично.',
                             reply_markup=go_to_menu())
            bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)

    # ====КОНЕЦ БЛОКА РАССЫЛКИ====