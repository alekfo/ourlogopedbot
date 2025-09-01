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


def reg_clients_handlers(bot):

    # ========ИНФОРМАЦИОННЫЙ БЛОК КЛИЕНТА===========
    @bot.message_handler(state=reg_states_client.in_any_block, func=lambda message: message.text == 'Информация')
    def information(message: Message):
        bot.send_message(message.chat.id,
                         'Этот бот дает возможность смотреть и управлять своим расписанием.\n'
                         'Для возврата в основное меню нажмите на кнопку ниже',
                         reply_markup=go_to_menu())
        bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)
    # ==========КОНЕЦ ИНФОРМАЦИОННОГО БЛОКА КЛИЕНТА=============

    # ========БЛОК РАСПИСАНИЯ КЛИЕНТА================
    @bot.message_handler(state=reg_states_client.in_any_block, func=lambda message: message.text == 'Расписание')
    def client_schedule(message: Message):
        bot.send_message(message.chat.id,
                         'Тут в дальнейшем можно будет посмотреть активное расписание',
                         reply_markup=go_to_menu())
        bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)
# ========КОНЕЦ БЛОКА РАСПИСАНИЯ КЛИЕНТА================

# ========БЛОК ОБРАТНОЙ СВЯЗИ КЛИЕНТА================
    @bot.message_handler(state=reg_states_client.in_any_block,
                         func=lambda message: message.text == 'Отзывы и предложения')
    def feedback(message: Message):
        bot.send_message(message.chat.id,
                         'Тут в дальнейшем можно будет оставить отзыв',
                         reply_markup=go_to_menu())
        bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)
# ========КОНЕЦ БЛОКА ОБРАТНОЙ СВЯЗИ КЛИЕНТА===========