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
    downloads_type)

def reg_downloads_handlers(bot: TeleBot):
    # ========БЛОК ВЫБОРА ТИПА ВЫГРУЗКИ===========
    @bot.message_handler(state=reg_states_admin.in_any_block,
                         func=lambda message: message.text == 'Выгрузка данных')
    def downloads_actions(message: Message):
        bot.send_message(message.chat.id,
                         'Выберите тип выгрузки',
                         reply_markup=downloads_type())
        bot.set_state(message.from_user.id, reg_states_admin.in_downloads, message.chat.id)
    # ========БЛОК ВЫБОРА ТИПА ВЫГРУЗКИ===========

    #=======НАЧАЛО Вернуться в основное меню=======#
    @bot.message_handler(state=reg_states_admin.in_downloads,
                         func=lambda message: message.text == 'Вернуться в основное меню')
    def return_to_menu(message: Message):
        bot.send_message(message.chat.id,
                         'Выберите действие',
                         reply_markup=main_admin_commands())
        bot.set_state(message.from_user.id, reg_states_admin.in_any_block, message.chat.id)
    # ======= КОНЕЦ Вернуться в основное меню=======#



    # ========БЛОК ВЫГРУЗКИ ДАННЫХ ОБ АКТИВНЫХ КЛИЕНТАХ===========
    @bot.message_handler(state=reg_states_admin.in_downloads,
                         func=lambda message: message.text == 'Данные активных клиентов')
    def downloads_clients(message: Message):
        try:
            clients_data = Client.select()
            weeks = Week.select()

            # Создаем Excel файл в памяти
            workbook = openpyxl.Workbook()
            clients_sheet = workbook.active
            clients_sheet.title = 'Дынные клиентов'

            # Заполняем лист с данными активных клиентов
            headers = ['№ п/п', 'ID клиента', 'Имя', 'Фамилия', 'Номер телефона', 'Имя ребенка', 'Дата рождения ребенка']
            for col_num, header in enumerate(headers, 1):
                clients_sheet.cell(row=1, column=col_num, value=header)

            for i_index, i_client in enumerate(clients_data, 2):
                clients_sheet.cell(row=i_index, column=1, value=i_index - 1)
                clients_sheet.cell(row=i_index, column=2, value=i_client.clients_id)
                clients_sheet.cell(row=i_index, column=3, value=i_client.clients_name)
                clients_sheet.cell(row=i_index, column=4, value=i_client.clients_sirname)
                clients_sheet.cell(row=i_index, column=5, value=i_client.clients_number)
                clients_sheet.cell(row=i_index, column=6, value=i_client.clients_child_name)
                clients_sheet.cell(row=i_index, column=7, value=i_client.clients_child_birthday)

            # Заполняем листы с расписаниями

            excel_file = BytesIO()
            workbook.save(excel_file)
            excel_file.seek(0)

            bot.send_document(message.chat.id,
                              document=excel_file,
                              visible_file_name='output_data_clients.xlsx',
                              caption='В файле "output_data_clients.xlsx" выгрузка из базы данных по активным клиентам',
                              reply_markup=go_to_menu())

            bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Ошибка при выгрузке: {str(e)}")
    # ========КОНЕЦ БЛОКА ВЫГРУЗКИ ДАННЫХ ОБ АКТИВНЫХ КЛИЕНТАХ===========

    # ========БЛОК ПОЛУЧЕНИЯ ДАТЫ ПОНЕДЕЛЬНИКА===========
    @bot.message_handler(state=reg_states_admin.in_downloads,
                         func=lambda message: message.text == 'Расписания')
    def downloads_actions(message: Message):
        bot.send_message(message.chat.id,
                         'Пришлите дату понедельника недели для выгрузки. Формат - DD.MM.YYYY',
                         reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.from_user.id, reg_states_admin.in_downloads_schedule, message.chat.id)
    # ========КОНЕЦ БЛОКА ПОЛУЧЕНИЯ ДАТЫ ПОНЕДЕЛЬНИКА===========

    # ========БЛОК ВЫГРУЗКИ ДАННЫХ О РАСПИСАНИИ===========
    @bot.message_handler(state=reg_states_admin.in_downloads_schedule)
    def downloads_clients(message: Message):
        try:
            #НЕОБХОДИМО ДОБАВИТЬ ПРОВЕРКУ ФОРМАТА ДАТЫ
            input_date = datetime.strptime(message.text, '%d.%m.%Y').date()
            week = Week.get(Week.monday_date == input_date)
            next_day = week.monday_date
            lessons = week.lessons

            # Создаем Excel файл в памяти
            workbook = openpyxl.Workbook()
            schedule_sheet = workbook.active
            schedule_sheet.title = f'Расписание {week.monday_date}'

            # Заполняем лист с данными запрошенного расписания
            headers = ['День недели',
                       'Дата',
                       '8:00',
                       '8:45',
                       '9:30',
                       '10:15',
                       '11:00',
                       '11:45',
                       '12:30',
                       '13:15',
                       '17:30',
                       '18:15',
                       '19:00'
                       ]
            for col_num, header in enumerate(headers, 1):
                schedule_sheet.cell(row=1, column=col_num, value=header)

            for i_row in range(2, 8):
                schedule_sheet.cell(row=i_row, column=1, value=Lesson.days_dict[i_row - 2])
                schedule_sheet.cell(row=i_row, column=2, value=next_day)
                for i_lesson in lessons:
                    if i_lesson.day_of_week == i_row - 2:
                        client_data = [i_lesson.client.clients_name, i_lesson.client.clients_sirname]
                        schedule_sheet.cell(row=i_row, column=i_lesson.lesson_number + 2, value=' '.join(client_data))
                next_day += timedelta(days=1)

            schedule_sheet.cell(row=8, column=1, value='Дата понедельника: ')
            schedule_sheet.cell(row=8, column=2, value=input_date)

            excel_file = BytesIO()
            workbook.save(excel_file)
            excel_file.seek(0)

            bot.send_document(message.chat.id,
                              document=excel_file,
                              visible_file_name='output_data_schedule.xlsx',
                              caption=f'В файле "output_data_schedule.xlsx" вся выгрузка из базы данных за выбранную ({message.text}) неделю',
                              reply_markup=go_to_menu())

            bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Ошибка при выгрузке: {str(e)}")
    # ========БЛОК ВЫГРУЗКИ ДАННЫХ О РАСПИСАНИИ===========