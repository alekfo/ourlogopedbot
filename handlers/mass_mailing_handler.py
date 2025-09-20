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
    """
    Функция для регистрации обработчиков для массовой рассылки всем активным клинтам
    :param bot: переменная с приложением
    :return: None
    """

    @bot.message_handler(state=reg_states_admin.in_any_block,
                         func=lambda message: 'Сделать рассылку' in message.text)
    def get_message(message: Message):
        """
        Обработчик состояния in_any_block при нажатии на кнопку "Сделать рассылку".
        Предлагает пользователю отправить сообщение для массовой рассылки.
        Дает возможность вернуться в основное меню кнопкой "Перейти в основное меню".
        Меняет состояние пользователя на reg_states_admin.mass_mailing_state
        :param message: переменная с приложением
        :return: None
        """

        bot.send_message(message.chat.id,
                        'Напишите сообщение\n<b>ПРЕДУПРЕЖДЕНИЕ</b>: данное сообщение отправится <b>всем зарегистрированным</b> клиентам\n'
                        'Для отмены нажмите на кнопку <b>Перейти в основное меню</b>',
                        reply_markup=go_to_menu(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_admin.mass_mailing_state, message.chat.id)

    @bot.message_handler(state=reg_states_admin.mass_mailing_state)
    def mass_mailing(message: Message):
        """
        Обработчкик состояния после отправки админом сообщения для массовой рассылки.
        Выбирает из базы данных всех активных клинтов.
        Отправлет всем активным клиентам сообщение от админа.
        Отправляет в ответ админу подтверждение об отправке рассылки.
        Меняет состояние на reg_states_admin.admin_menu
        :param message: переменная с приложением
        :return: None
        """

        clients = Client.select()
        for i_client in clients:
            bot.send_message(i_client.clients_chat_id, message.text)
        bot.send_message(message.chat.id,
                         'Сообщение отправлено всем пользователям✅\nПри ошибочной отправке рекомендуется обратиться к клиентам лично.',
                         reply_markup=go_to_menu(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)