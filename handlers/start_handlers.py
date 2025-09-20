from peewee import DoesNotExist
from telebot import TeleBot
from telebot.types import Message
from config import admin_id
from DATABASE.peewee_config import Client
from states import reg_states_client, reg_states_admin
from keyboards.main_keyboards import (
    start_registration,
    go_to_menu)

def reg_start_handlers(bot: TeleBot):
    """
    Функция для регистрации обработчика первого стартового сообщения
    :param bot: переменная с приложением
    :return: None
    """

    @bot.message_handler(state=None, func=lambda message: True)
    def first_message(message: Message):
        """
        Обработчик фиксирует любые сообщения, когда сценарий еще не запущен и состояние не задано.
        Функция делает запрос к базе данных для получения модели пользователя. При подтверждении регистрации
        пользователю отправляется приветственное сообщение с предложением пройти в основное меню, состояние
        пользователя меняется на reg_states_client.in_menu.
        При отсутствии пользователя в базе даных проверяется, является ли пользователь администратором: если не является -
        отправляется приветственное сообщение с предложением пройти регистрацию по кнопке, состояние меняется на reg_states_client.start_registration;
        если пользователь является администратором - предлагается пройти в основное меню администратора, состояние пользователя меняется ан
        reg_states_admin.admin_menu
        :param message: сообщения от пользователя;
        :return: None
        """

        try:
            client = Client.get(Client.clients_id == message.from_user.id)
            bot.send_message(message.chat.id,
                             f'Рад снова видеть Вас, {client.clients_name}!👋\n'
                                              f'Для перехода в меню нажми на кнопку ниже',
                             reply_markup=go_to_menu(), parse_mode='HTML'
                             )
            bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)
        except DoesNotExist:
            if message.from_user.id != admin_id:
                bot.send_message(message.chat.id,
                                 'Добро пожаловать в чат-бот центра "ЛОГОПЕДиЯ"!🦄👨‍👩‍👧‍👦\n'
                                                  'Чтобы продолжить - пройдите регистрацию по кнопке ниже',
                                 reply_markup=start_registration(), parse_mode='HTML')
                bot.set_state(message.from_user.id, reg_states_client.start_registration, message.chat.id)
            else:
                bot.send_message(message.chat.id,
                                 'Вы являетесь администратором🥷 чата, нажмите на кнопку ниже для прохода в меню',
                                 reply_markup=go_to_menu(), parse_mode='HTML'
                                 )
                bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)


