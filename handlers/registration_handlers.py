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

def reg_registration_handlers(bot: TeleBot):
    # =====БЛОК РЕГИСТРАЦИИ КЛИЕНТА==========
    @bot.message_handler(state=reg_states_client.start_registration)
    def start_reg(message: Message):
        bot.send_message(message.chat.id, 'Отправьте Ваше имя', reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.from_user.id, reg_states_client.getting_name, message.chat.id)

    @bot.message_handler(state=reg_states_client.getting_name)
    def got_name(message: Message):
        if message.text.isalpha():
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['name'] = message.text
            bot.send_message(message.chat.id, 'Спасибо, записал! Теперь пришлите Вашу фамилию')
            bot.set_state(message.from_user.id, reg_states_client.getting_sirname, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Имя должно состоять только из букв. Пришли корректное имя')

    @bot.message_handler(state=reg_states_client.getting_sirname)
    def got_sirname(message: Message):
        if message.text.isalpha():
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['sirname'] = message.text
            bot.send_message(message.chat.id,
                             'Спасибо, записал! Теперь мне нужен Ваш номер телефона.\n'
                             'Для отправки номера телефона воспользуйтесь кнопкой ниже',
                             reply_markup=get_contact(), parse_mode='HTML'
                             )
            bot.set_state(message.from_user.id, reg_states_client.getting_number, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Фамилия должна состоять только из букв. Пришли корректную фамилию')

    @bot.message_handler(content_types=['contact'])
    def got_contact(message):
        # message.contact - объект с данными контакта
        phone_number = message.contact.phone_number
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['number'] = phone_number
        bot.send_message(
            message.chat.id,
            f"Отлично! Телефон записал. Теперь пришлите имя и фамилия Вашего ребенка (через пробел)",
            reply_markup=ReplyKeyboardRemove()  # Убираем клавиатуру
        )
        bot.set_state(message.from_user.id, reg_states_client.getting_child_name, message.chat.id)

    @bot.message_handler(state=reg_states_client.getting_number)
    def wrong_number(message: Message):
        bot.send_message(message.chat.id,
                         'Для отправки номера телефона необходимо воспользоваться кнопкой ниже',
                         reply_markup=get_contact(), parse_mode='HTML'
                         )

    @bot.message_handler(state=reg_states_client.getting_child_name)
    def got_child_name(message: Message):
        if len(message.text.split()) == 2:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['child_name'] = message.text
            bot.send_message(message.chat.id,
                             'Записал! Теперь пришлите дату рождения Вашего ребенка\n'
                             'Формат даты: DD.MM.YYYY')
            bot.set_state(message.from_user.id, reg_states_client.getting_child_birthday, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Имя и фамилию ребенка необходимо написать через пробел')

    @bot.message_handler(state=reg_states_client.getting_child_birthday)
    def got_child_birthday(message: Message):
        format_list = message.text.split('.')
        if len(format_list) == 3 and 0 < int(format_list[0]) <= 31 and 0 < int(format_list[1]) <= 12 and 0 < int(
                format_list[2]):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['child_birthday'] = message.text
                Client.create(
                    clients_id=message.from_user.id,
                    clients_chat_id=message.chat.id,
                    clients_name=data['name'],
                    clients_sirname=data['sirname'],
                    clients_number=data['number'],
                    clients_child_name=data['child_name'],
                    clients_child_birthday=data['child_birthday']
                )
            bot.send_message(message.chat.id,
                             'Отлично! Все необходимые данные получены!\n'
                             'Для перехода в меню нажми на кнопку ниже',
                             reply_markup=go_to_menu(), parse_mode='HTML'
                             )
            bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Дата рождения должна быть формата DD.MM.YYYY')
# =========КОНЕЦ БЛОКА РЕГИСТРАЦИИ КЛИЕНТА=============