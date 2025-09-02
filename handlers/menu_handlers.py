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

def reg_menu_handlers(bot: TeleBot):
# ========БЛОК ОСНОВНОГО МЕНЮ КЛИЕНТА=========
    @bot.message_handler(state=reg_states_client.in_menu)
    def show_client_cmd(message: Message):
        output_txt = 'Доступные команды: \n\n'
        output_txt += '/info - Показать информацию о возможностях бота\n'
        output_txt += '/schedule - Посмотреть свое расписание\n'
        output_txt += '/feedback - Оставить отзыв или предложения\n'

        bot.send_message(message.chat.id, output_txt, reply_markup=main_clients_commands())
        bot.set_state(message.from_user.id, reg_states_client.in_any_block, message.chat.id)
    # ========КОНЕЦ БЛОКА ОСНОВНОГО МЕНЮ КЛИЕНТА=========

    # ========НАЧАЛО БЛОКА МЕНЮ АДМИНА=========
    @bot.message_handler(state=reg_states_admin.admin_menu)
    def admin_menu(message: Message):
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=main_admin_commands())
        bot.set_state(message.from_user.id, reg_states_admin.in_any_block, message.chat.id)
# ========КОНЕЦ БЛОКА МЕНЮ АДМИНА=========