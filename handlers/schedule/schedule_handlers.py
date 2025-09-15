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


def reg_schedule_handlers(bot: TeleBot):

# ========БЛОК ВЫБОРА ДЕЙСТВИЯ НАД РАСПИСАНИЕМ===========
    @bot.message_handler(state=reg_states_admin.in_any_block,
                         func=lambda message: message.text == 'Управление расписанием')
    def schedule_actions(message: Message):
        bot.send_message(message.chat.id,
                         'Выберите действие с расписанием',
                         reply_markup=schedule_menu())
        bot.set_state(message.from_user.id, reg_states_admin.in_schedule, message.chat.id)
# ========КОНЕЦ БЛОКА ВЫБОРА ДЕЙСТВИЯ НАД РАСПИСАНИЕМ===========

#====НАЧАЛО БЛОКА ОТМЕНЫ=++===
    @bot.message_handler(state= [reg_states_admin.in_schedule,
                                 reg_states_admin.process_file,
                                 reg_states_admin.show_schedule],
                        func=lambda message: message.text == 'Перейти в основное меню')
    def return_to_menu(message: Message):
        bot.send_message(message.chat.id,
                         'Выберите действие',
                         reply_markup=main_admin_commands())
        bot.set_state(message.from_user.id, reg_states_admin.in_any_block, message.chat.id)
#====КОНЕЦ БЛОКА ОТМЕНЫ=++===


# ========ДОБАВЛЕНИЕ РАСПИСАНИЯ===========
    @bot.message_handler(state=reg_states_admin.in_schedule,
                         func=lambda message: message.text == 'Добавить расписание')
    def add_schedule(message: Message):
        bot.send_message(message.chat.id,
                         'Отправьте файл формата .xlsx\n'
                         'В строках файла должны содержаться дни недели (кроме воскресенья),\n'
                         'в столбцах - разбивка по урокам\n\n'
                         'Для избежания ошибок при загрузке рекомендуется ознакомиться с образцом загрузочного файла',
                         reply_markup=go_to_menu())
        bot.set_state(message.from_user.id, reg_states_admin.process_file, message.chat.id)
# ========КОНЕЦ БЛОКА ДОБАВЛЕНИЯ РАСПИСАНИЯ===========

# ========ОБРАБОТКА ФАЙЛА===========
    @bot.message_handler(content_types=['document'], state=reg_states_admin.process_file)
    def file_procced(message: Message):
        try:
            # Получаем информацию о файле
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            # Создаем BytesIO объект для работы с файлом в памяти
            excel_data = BytesIO(downloaded_file)

            # Загружаем Excel файл в
            workbook = openpyxl.load_workbook(excel_data)
            sheet = workbook.active
            monday_data = sheet.cell(2, 2).value                        #забираем значение из ячейки
            # formated_data = datetime.strptime(monday_data, "%d.%m.%Y").date()      #преобразуем в DateField
            Week.delete().where(Week.monday_date == monday_data).execute()                  # Удаляем для избежания повтора уникальности
            curr_week = Week.create(monday_date=monday_data)
            Lesson.delete().where(Lesson.weekly_schedule == curr_week).execute()
            for i_row in range(2, 8):
                for i_col in range(3, 14):
                    cell = sheet.cell(i_row, i_col).value
                    if cell is None:
                        continue
                    else:
                        cell_list = cell.split()
                        name, sirname = cell_list
                        curr_client = Client.get_or_none((Client.clients_name == name) & (Client.clients_sirname == sirname))
                        if curr_client:
                            Lesson.create(
                                lesson_date=sheet.cell(row=i_row, column=2).value,
                                weekly_schedule=curr_week,
                                client=curr_client,
                                day_of_week=i_row - 2,
                                lesson_number=i_col - 2
                            )
                        else:
                            raise TypeError(f'В расписание добавлен не зарегистрированный пользователь - {cell}. '
                                            'Проверьте файл')
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Ошибка при обработке файла: {str(e)}", reply_markup=go_to_menu())
            bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)
        else:
            output_str = 'Данные успешно добавлены✅ \nРасписание текущей недели:\n'
            lessons_list = Lesson.select().where(Lesson.weekly_schedule == curr_week)
            lesson_dict = {}
            for i_less in lessons_list:
                if i_less.days_dict.get(i_less.day_of_week) in lesson_dict:
                    lesson_dict[i_less.days_dict.get(i_less.day_of_week)].append([
                        i_less.lessons_dict.get(i_less.lesson_number),
                        i_less.client.clients_name,
                        i_less.client.clients_sirname])
                else:
                    lesson_dict[i_less.days_dict.get(i_less.day_of_week)] = []
                    lesson_dict[i_less.days_dict.get(i_less.day_of_week)].append([
                        i_less.lessons_dict.get(i_less.lesson_number),
                        i_less.client.clients_name,
                        i_less.client.clients_sirname])
            for i_day, lessons in lesson_dict.items():
                output_str += '\n' + i_day + '\n'
                for i_less in lessons:
                    output_str += f'{i_less[0]} - {i_less[1]} {i_less[2]}\n'
            bot.send_message(message.chat.id, output_str, reply_markup=go_to_menu())
            bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)
# ========КОНЕЦ ОБРАБОТКИ ФАЙЛА===========

# ========ЗАПРОС ДАТЫ НА ПОКАЗ РАСПИСАНИЯ===========
    @bot.message_handler(state=reg_states_admin.in_schedule,
                         func=lambda message: message.text == 'Посмотреть расписание')
    def show_schedule(message: Message):
        bot.send_message(message.chat.id,
                         'Пришлите дату понедельника недели, расписание которой хотите посмотреть\n'
                         'Формат даты: DD.MM.YYYY',
                         reply_markup=go_to_menu())
        bot.set_state(message.from_user.id, reg_states_admin.show_schedule, message.chat.id)
# ========КОНЕЦ БЛОКА ЗАПРОСА ДАТЫ ПОКАЗАТЬ РАСПИСАНИЕ===========

# ========ПОКАЗ РАСПИСАНИЯ===========
    @bot.message_handler(state=reg_states_admin.show_schedule)
    def show_schedule(message: Message):
        check_format_list = message.text.split('.')
        try:
            if len(check_format_list) == 3 and 0 < int(check_format_list[0]) <= 31 and 0 < int(check_format_list[1]) <= 12 and int(check_format_list[2]) > 0:
                formated_data = datetime.strptime(message.text, "%d.%m.%Y").date()
                curr_week = Week.get_or_none(Week.monday_date == formated_data)
                lesson_list = curr_week.lessons
                output_str = f'Расписание текущей ({curr_week}) недели:\n'
                lesson_dict = {}
                for i_less in lesson_list:
                    if i_less.days_dict.get(i_less.day_of_week) in lesson_dict:
                        lesson_dict[i_less.days_dict.get(i_less.day_of_week)].append([
                            i_less.lessons_dict.get(i_less.lesson_number),
                            i_less.client.clients_name,
                            i_less.client.clients_sirname])
                    else:
                        lesson_dict[i_less.days_dict.get(i_less.day_of_week)] = []
                        lesson_dict[i_less.days_dict.get(i_less.day_of_week)].append([
                            i_less.lessons_dict.get(i_less.lesson_number),
                            i_less.client.clients_name,
                            i_less.client.clients_sirname])
                for i_day, lessons in lesson_dict.items():
                    output_str += '\n' + i_day + '\n'
                    for i_less in lessons:
                        output_str += f'{i_less[0]} - {i_less[1]} {i_less[2]}\n'
                bot.send_message(message.chat.id,
                                 output_str, reply_markup=go_to_menu())
                bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)
            else:
                raise TypeError('Введите данные формата DD.MM.YYYY')
        except Exception as e:
            bot.send_message(message.chat.id,f'{e} - Введите данные формата DD.MM.YYYY')
# ========КОНЕЦ БЛОКА ПОКАЗ РАСПИСАНИЯ===========