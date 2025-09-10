from peewee import IntegrityError, DoesNotExist
from datetime import datetime
import telebot
from telebot import TeleBot
from telebot.types import Message, BotCommand, ReplyKeyboardRemove
from config import admin_id
from DATABASE.peewee_config import Client, Week, Lesson, Feedback
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
        current_date = datetime.now().date()
        curr_client = Client.get_or_none(Client.clients_id == message.from_user.id)
        lessons = curr_client.lessons
        active_lessons = [
            i_lesson
            for i_lesson in lessons
            if i_lesson.lesson_date >= current_date
        ]
        if not active_lessons:
            bot.send_message(message.chat.id, "У вас нет запланированных занятий", reply_markup=go_to_menu())
            bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)
        else:
            output_str = 'Вот ваше расписание🗓️:\n\n'
            for i_les in active_lessons:
                output_str += f'{i_les.days_dict.get(i_les.day_of_week, 'Неизвестный день')} - {i_les.lessons_dict.get(i_les.lesson_number, 'Неизвестное время')}\n'
            bot.send_message(message.chat.id,
                             output_str,
                             reply_markup=go_to_menu())
            bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)
# ========КОНЕЦ БЛОКА РАСПИСАНИЯ КЛИЕНТА================

# ========БЛОК ОБРАТНОЙ СВЯЗИ КЛИЕНТА================
    @bot.message_handler(state=reg_states_client.in_any_block,
                         func=lambda message: message.text == 'Отзывы и предложения')
    def feedback(message: Message):
        bot.send_message(message.chat.id,
                         'Отправьте текст с отзывом. Мы рады любой критике и ценим ваше мнение!\n'
                         'Если хотите вернуться в меню - нажмите на кнопку ниже',
                         reply_markup=go_to_menu())
        bot.set_state(message.from_user.id, reg_states_client.get_feedback, message.chat.id)
# ========КОНЕЦ БЛОКА ОБРАТНОЙ СВЯЗИ КЛИЕНТА===========

# ========ОБРАБОТКА СООБЩЕНИЯ ОБРАТНОЙ СВЯЗИ================
    @bot.message_handler(state=reg_states_client.get_feedback)
    def feedback(message: Message):
        if message.text == 'Перейти в основное меню':
            output_txt = 'Доступные команды: \n\n'
            output_txt += 'Информация❓ - Показать информацию о возможностях бота\n'
            output_txt += 'Расписание🗓️ - Посмотреть свое расписание\n'
            output_txt += 'Отзывы и предложения💾 - Оставить отзыв или предложения\n'
            bot.send_message(message.chat.id, output_txt, reply_markup=main_clients_commands())
            bot.set_state(message.from_user.id, reg_states_client.in_any_block, message.chat.id)
        else:
            curr_client = Client.get_or_none(Client.clients_id == message.from_user.id)
            Feedback.create(
                client=curr_client,
                text=message.text,
                feedback_date=datetime.now()
            )
            bot.send_message(message.chat.id,
                             'Спасибо за оставленный комментарий💔! Мы очень ценим это!',
                             reply_markup=go_to_menu())
            bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)
            try:
                curr_feedback = Feedback.get_or_none(Feedback.client == curr_client)
                date = curr_feedback.feedback_date
                text = message.text
                bot.send_message(admin_id,
                                 f'Оставлен новый отзыв:\n\n'
                                 f'Текст: "{text}"\n'
                                 f'Кто оставил: {curr_client.clients_name} {curr_client.clients_sirname}',
                                 reply_markup=go_to_menu())
            except Exception as e:
                print('Ошибка отправки админу отзыва:', e)
# ========КОНЕЦ ОБРАБОТКИ СООБЩЕНИЯ ОБРАТНОЙ СВЯЗИ===========

#=====Обработка подтверждения урока=====
    @bot.callback_query_handler(
        func=lambda callback_query: (
            callback_query.data == "confirmed"
        )
    )
    def confirmed(callback_query):
        # Удаляем клавиатуру.
        bot.edit_message_reply_markup(
            callback_query.from_user.id, callback_query.message.message_id
        )
        # Отправляем сообщение пользователю.
        bot.send_message(
            callback_query.from_user.id,
            "Ждем Вас к назначенному часу!",
        )
        curr_client = Client.get_or_none(Client.clients_id == callback_query.from_user.id)
        message_to_admin = f'{curr_client.clients_name} {curr_client.clients_sirname} подтвердил ближайшую запись!'
        bot.send_message(
            admin_id,
            message_to_admin,
        )

        @bot.callback_query_handler(
            func=lambda callback_query: (
                    callback_query.data == "canceled"
            )
        )
        def canceled(callback_query):
            # Удаляем клавиатуру.
            bot.edit_message_reply_markup(
                callback_query.from_user.id, callback_query.message.message_id
            )
            # Отправляем сообщение пользователю.
            bot.send_message(
                callback_query.from_user.id,
                "Спасибо, что уведомили! Свяжитесь с учителем, чтобы назначить дату нового занятия!",
            )
            curr_client = Client.get_or_none(Client.clients_id == callback_query.from_user.id)
            message_to_admin = f'{curr_client.clients_name} {curr_client.clients_sirname} ОТМЕНИЛ ближайшую запись!'
            bot.send_message(
                admin_id,
                message_to_admin,
            )
#=====Обработка подтверждения урока=====