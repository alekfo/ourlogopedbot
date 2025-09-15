from logging import raiseExceptions

from peewee import IntegrityError, DoesNotExist
import telebot
from datetime import datetime, timedelta
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
    schedule_menu,
    choise_action,
    lessons_markup,
    confirmation_in_schedule,
    days_markup)

def reg_menage_schedule_handlers(bot: TeleBot):
    # ====НАЧАЛО БЛОКА ОТМЕНЫ=++===
    @bot.message_handler(state=[reg_states_admin.in_schedule,
                                reg_states_admin.get_lesson_number,
                                reg_states_admin.delete_confirmation,
                                reg_states_admin.create_lesson],
                         func=lambda message: message.text == 'Перейти в основное меню')
    def return_to_menu(message: Message):
        bot.send_message(message.chat.id,
                         'Выберите действие',
                         reply_markup=main_admin_commands())
        bot.set_state(message.from_user.id, reg_states_admin.in_any_block, message.chat.id)
    # ====КОНЕЦ БЛОКА ОТМЕНЫ=++===

    #Выбор действия
    @bot.message_handler(state=reg_states_admin.in_schedule,
                         func=lambda message: message.text == 'Изменить расписание')
    def choising_action(message: Message):
        bot.send_message(message.chat.id,
                         'Что хотите сделать?',
                         reply_markup=choise_action())
        bot.set_state(message.from_user.id, reg_states_admin.choisen_action, message.chat.id)
    #Конец выбора действия

    #Выбор дня недели
    @bot.message_handler(state=reg_states_admin.choisen_action)
    def getting_weekday(message: Message):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['action'] = message.text
        bot.send_message(message.chat.id,
                         'Какой день недели?',
                         reply_markup=days_markup())
        bot.set_state(message.from_user.id, reg_states_admin.get_weekday, message.chat.id)
    # Конец Выбора дня недели

    # ========Выбор урока в удалении===========
    @bot.message_handler(state=reg_states_admin.get_weekday)
    def getting_lessons_number(message: Message):
        lessons_dict = {
            'Понедельник': 0,
            'Вторник': 1,
            'Среда': 2,
            'Четверг': 3,
            'Пятница': 4,
            'Суббота': 5
        }
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['weekday'] = lessons_dict.get(message.text)
        bot.send_message(message.chat.id,
                         'Теперь выберите время урока',
                         reply_markup=lessons_markup())
        bot.set_state(message.from_user.id, reg_states_admin.get_lesson_number, message.chat.id)
    # ========КОНЕЦ БЛОКА===========

    # ========Удаление или добавление===========
    @bot.message_handler(state=reg_states_admin.get_lesson_number)
    def delete_lesson(message: Message):
        lessons_dict = {
            '8:00': 1,
            '8:45': 2,
            '9:30': 3,
            '10:15': 4,
            '11:00': 5,
            '11:45': 6,
            '12:30': 7,
            '13:15': 8,
            '17:30': 9,
            '18:15': 10,
            '19:00': 11,
        }
        choisen_lesson = lessons_dict.get(message.text)
        last_week = Week.select().order_by(Week.schedule_id.desc()).first()


        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            curr_weekday = data['weekday']
            action = data['action']
            data['week'] = last_week
            data['lesson'] = choisen_lesson
            date_of_lesson = last_week.monday_date + timedelta(days=curr_weekday)
            data['date_of_lesson'] = date_of_lesson

        curr_lesson = Lesson.get_or_none(Lesson.lesson_number == choisen_lesson,
                                         Lesson.weekly_schedule == last_week,
                                         Lesson.day_of_week == curr_weekday)
        if action == 'Удалить урок':
            if curr_lesson:
                curr_client = curr_lesson.client
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data['client_to_delete'] = curr_client

                bot.send_message(message.chat.id,
                                 f'На это время есть активная запись: {curr_client.clients_name} {curr_client.clients_sirname}\n'
                                 f'Вы подтверждаете, что хотите удалить данного клиента с указанного урока ({message.text})?',
                                 reply_markup=confirmation_in_schedule())
                bot.set_state(message.from_user.id, reg_states_admin.delete_confirmation, message.chat.id)
            else:
                bot.send_message(message.chat.id,
                                 f'На это время никого нет. Выберите другое время',
                                 reply_markup=lessons_markup())
        elif action == 'Добавить урок':
            if curr_lesson:
                bot.send_message(message.chat.id,
                                 f'Это время занято. Выберите другое время',
                                 reply_markup=lessons_markup())
            else:
                bot.send_message(message.chat.id,
                                 f'Кого хотите записать на это время? Напишите имя и фамилию через пробел',
                                 reply_markup=ReplyKeyboardRemove())
                bot.set_state(message.from_user.id, reg_states_admin.create_lesson, message.chat.id)
    # ========КОНЕЦ БЛОКА===========


    #Добавление урока
    @bot.message_handler(state=reg_states_admin.create_lesson)
    def adding_lesson(message: Message):
        try:
            name_sirname = message.text.split()
            if len(name_sirname) != 2:
                raise DoesNotExist('клиента с таким именем не существует.\nИмя и фамилия должны быть написаны с большой буквы через пробел\n'
                                   'Пришлите имя и фамилию еще раз')
            curr_client = Client.get_or_none(Client.clients_name == name_sirname[0],
                                             Client.clients_sirname == name_sirname[1])
            if curr_client is None:
                raise DoesNotExist('клиента с таким именем не существует.\nИмя и фамилия должны быть написаны с большой буквы через пробел\n'
                                   'Пришлите имя и фамилию еще раз')
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                curr_weekday = data['weekday']
                action = data['action']
                last_week = data['week']
                choisen_lesson = data['lesson']
                date_of_lesson = data['date_of_lesson']
            try:
                Lesson.create(
                    lesson_date=date_of_lesson,
                    weekly_schedule=last_week,
                    client=curr_client,
                    day_of_week=curr_weekday,
                    lesson_number=choisen_lesson
                )
                bot.send_message(message.chat.id,
                                 f'Клиент записан!✅\n\n'
                                 f'{Lesson.days_dict.get(curr_weekday)}, '
                                 f'{Lesson.lessons_dict.get(choisen_lesson)} - {curr_client.clients_name} {curr_client.clients_sirname}',
                                 reply_markup=go_to_menu())
                bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data.clear()  # Очищаем весь словарь
            except Exception as e:
                bot.send_message(message.chat.id,
                                 f'Ошибка при сохранении клиента. ПОпробуйте снова.\n'
                                 f'Выберите действие',
                                 reply_markup=choise_action())
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data.clear()  # Очищаем весь словарь
                bot.set_state(message.from_user.id, reg_states_admin.choisen_action, message.chat.id)
        except DoesNotExist as e:
            bot.send_message(message.chat.id, f"❌ Ошибка при добавлении урока: {str(e)}\n"
                                              f"Если хотите вернуться в основное меню - нажмите на кнопку ниже", reply_markup=go_to_menu())

    #БЛОК Подтверждения удаления
    @bot.message_handler(state=reg_states_admin.delete_confirmation,
                         func=lambda message: message.text == 'Подтверждаю✅')
    def confirm_delete(message: Message):
        try:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                curr_client = data['client_to_delete']
                last_week = data['week']
                choisen_lesson = data['lesson']
                curr_weekday = data['weekday']

            lesson_to_delete = Lesson.get(
                (Lesson.lesson_number == choisen_lesson) &
                (Lesson.client == curr_client) &
                (Lesson.weekly_schedule == last_week) &
                (Lesson.day_of_week == curr_weekday)
            )
            deleted_count = lesson_to_delete.delete_instance()

            if deleted_count == 0:
                bot.send_message(message.chat.id,
                                 'Ошибка удаления. Попробуйте снова',
                                 reply_markup=lessons_markup())
                bot.set_state(message.from_user.id, reg_states_admin.delete_lesson, message.chat.id)
            else:
                bot.send_message(message.chat.id,
                                 f'{curr_client.clients_name} {curr_client.clients_sirname} успешно удален✅',
                                 reply_markup=go_to_menu())
                bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data.clear()  # Очищаем весь словарь

        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Ошибка при подтверждении удаления: {str(e)}\n"
                                              f"Для возврата в меню воспользуйтесь кнопкой ниже",
                             reply_markup=go_to_menu())
            bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)



