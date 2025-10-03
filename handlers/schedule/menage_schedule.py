from peewee import DoesNotExist
from datetime import timedelta
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from DATABASE.peewee_config import Client, Week, Lesson
from states import reg_states_admin
from keyboards.main_keyboards import (
    go_to_menu,
    main_admin_commands,
    choise_action,
    lessons_markup,
    confirmation_in_schedule,
    days_markup)

def reg_menage_schedule_handlers(bot: TeleBot):
    """
    Функция для регистрации обработчиков для управления расписанием
    :param bot: переменная с приложением
    :return: None
    """

    @bot.message_handler(state=[reg_states_admin.in_schedule,
                                reg_states_admin.get_lesson_number,
                                reg_states_admin.delete_confirmation,
                                reg_states_admin.create_lesson,
                                reg_states_admin.choisen_action],
                         func=lambda message: 'Перейти в основное меню' in message.text)
    def return_to_menu(message: Message):
        """
        Обработчик сообщения "Перейти в основное меню" состояний
                                reg_states_admin.in_schedule,
                                reg_states_admin.get_lesson_number,
                                reg_states_admin.delete_confirmation,
                                reg_states_admin.create_lesson,
                                reg_states_admin.choisen_action
        для возврата в основное меню, аналог обработчика admin_menu.
        Меняет состояние пользователя на reg_states_admin.in_any_block
        :param message: сообщения от пользователя
        :return: None
        """

        bot.send_message(message.chat.id,
                         'Выберите действие',
                         reply_markup=main_admin_commands(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_admin.in_any_block, message.chat.id)

    @bot.message_handler(state=reg_states_admin.in_schedule,
                         func=lambda message: 'Изменить расписание' in message.text)
    def choising_action(message: Message):
        """
        Обработчик состояния reg_states_admin.in_schedule при нажатии админом на кнопку "Изменить расписание".
        Запрашивает у пользователя действие на расписанием, предлагая нажать на соответствующую кнопку.
        Меняет состояние на reg_states_admin.choisen_action
        :param message: сообщения от пользователя
        :return: None
        """

        bot.send_message(message.chat.id,
                         'Что хотите сделать?',
                         reply_markup=choise_action(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_admin.choisen_action, message.chat.id)

    @bot.message_handler(state=reg_states_admin.choisen_action)
    def getting_weekday(message: Message):
        """
        Обработчик состояния пользователя reg_states_admin.choisen_action после выбора админом действия.
        Записывает во временный словарь выбранное действие.
        Предлагает админу выбрать, над каким днем недели тот хочет выполнить выбранное действие.
        Меняет состояние пользователя на reg_states_admin.get_weekday
        :param message: сообщения от пользователя
        :return: None
        """

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['action'] = message.text
        bot.send_message(message.chat.id,
                         'Какой день недели?',
                         reply_markup=days_markup(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_admin.get_weekday, message.chat.id)

    @bot.message_handler(state=reg_states_admin.get_weekday)
    def getting_lessons_number(message: Message):
        """
        Обработчик состояния пользователя reg_states_admin.get_weekday.
        Записывает во временный словарь выбранный день недели.
        Предлагает админу выбрать время урока для совершения выбранного действия.
        Меняет состояния пользователя на reg_states_admin.get_lesson_number
        :param message: сообщения от пользователя
        :return: None
        """

        lessons_dict = {
            '📆Понедельник': 0,
            '📆Вторник': 1,
            '📆Среда': 2,
            '📆Четверг': 3,
            '📆Пятница': 4,
            '📆Суббота': 5
        }
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['weekday'] = lessons_dict.get(message.text)
        bot.send_message(message.chat.id,
                         'Теперь выберите время урока',
                         reply_markup=lessons_markup(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_admin.get_lesson_number, message.chat.id)

    @bot.message_handler(state=reg_states_admin.get_lesson_number)
    def delete_lesson(message: Message):
        """
        Обработчик состояния пользователя reg_states_admin.get_lesson_number.
        Записывает во временный словарь полученное время урока.
        В зависимости от выбранного действия над расписанием либо:
        - выводит админу клиента, который записан на это время, и переводит пользователя в состояние reg_states_admin.delete_confirmation
        для подтверждения записи, или выводит сообщение о занятости данного слота с предложением выбрать другой день;
        - предлагает админу ввести имя и фамилию клиента для добавления урока и меняет состояние пользователя на reg_states_admin.create_lesson
        или выводит сообщение о занятости данного слота с предложением выбрать другой день.
        :param message: сообщения от пользователя
        :return: None
        """

        lessons_dict = {
            '🕗8:00': 1,
            '🕗8:45': 2,
            '🕗9:30': 3,
            '🕗10:15': 4,
            '🕗11:00': 5,
            '🕗11:45': 6,
            '🕗12:30': 7,
            '🕗13:15': 8,
            '🕗17:30': 9,
            '🕗18:15': 10,
            '🕗19:00': 11,
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
        if 'Удалить занятие' in action:
            if curr_lesson:
                curr_client = curr_lesson.client
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data['client_to_delete'] = curr_client

                bot.send_message(message.chat.id,
                                 f'На это время есть активная запись: {curr_client.clients_name} {curr_client.clients_sirname}\n'
                                 f'Вы подтверждаете, что хотите удалить данного клиента с указанного урока ({message.text})?',
                                 reply_markup=confirmation_in_schedule(), parse_mode='HTML')
                bot.set_state(message.from_user.id, reg_states_admin.delete_confirmation, message.chat.id)
            else:
                bot.send_message(message.chat.id,
                                 f'На это время никого нет. Выберите другое время',
                                 reply_markup=lessons_markup(), parse_mode='HTML')
        elif 'Добавить занятие' in action:
            if curr_lesson:
                bot.send_message(message.chat.id,
                                 f'Это время занято. Выберите другое время',
                                 reply_markup=lessons_markup(), parse_mode='HTML')
            else:
                bot.send_message(message.chat.id,
                                 f'Кого хотите записать на это время? Напишите имя и фамилию через пробел',
                                 reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
                bot.set_state(message.from_user.id, reg_states_admin.create_lesson, message.chat.id)

    @bot.message_handler(state=reg_states_admin.create_lesson)
    def adding_lesson(message: Message):
        """
        Обработчик состояния reg_states_admin.create_lesson.
        Проверяет введенные админом имя и фамилию на корректность и на наличие в БД данного клиента.
        Если все корректно  создает модель нового урока в БД с данным клиентом.
        Отправляет админу подтверждение об успешном создании урока.
        Отправляет клиенту сообщение об изменении личного расписания.
        Обрабатывает ошибки.
        Меняет состояние при успехе на reg_states_admin.admin_menu
        :param message: сообщения от пользователя
        :return: None
        """

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
                                 reply_markup=go_to_menu(), parse_mode='HTML')
                bot.send_message(curr_client.clients_chat_id,
                                 'Ваше расписание изменено⚠️. Для просмотра пройдите в раздел "Расписание"')
                bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data.clear()  # Очищаем весь словарь
            except Exception as e:
                bot.send_message(message.chat.id,
                                 f'Ошибка при сохранении клиента. ПОпробуйте снова.\n'
                                 f'Выберите действие',
                                 reply_markup=choise_action(), parse_mode='HTML')
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data.clear()  # Очищаем весь словарь
                bot.set_state(message.from_user.id, reg_states_admin.choisen_action, message.chat.id)
        except DoesNotExist as e:
            bot.send_message(message.chat.id, f"❌ Ошибка при добавлении урока: {str(e)}\n"
                                              f"Если хотите вернуться в основное меню - нажмите на кнопку ниже", reply_markup=go_to_menu(), parse_mode='HTML')

    @bot.message_handler(state=reg_states_admin.delete_confirmation,
                         func=lambda message: 'Подтверждаю' in message.text)
    def confirm_delete(message: Message):
        """
        Обработчик состояния reg_states_admin.delete_confirmation при подтверждении админом удаления нажатием на кнопку "Подтверждаю".
        Удаляет выбранный урок.
        Отправляет админу подтверждение удаления.
        Отправляет клиенту уведомление об изменении расписания.
        Обрабатывает ошибки.
        Меняет состояние пользователя на reg_states_admin.admin_menu
        :param message: сообщения от пользователя
        :return: None
        """

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
                                 reply_markup=lessons_markup(), parse_mode='HTML')
                bot.set_state(message.from_user.id, reg_states_admin.delete_lesson, message.chat.id)
            else:
                bot.send_message(message.chat.id,
                                 f'{curr_client.clients_name} {curr_client.clients_sirname} успешно удален✅',
                                 reply_markup=go_to_menu(), parse_mode='HTML')
                bot.send_message(curr_client.clients_chat_id,
                                 'Ваше расписание изменено⚠️. Для просмотра пройдите в раздел "Расписание"')
                bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data.clear()  # Очищаем весь словарь

        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Ошибка при подтверждении удаления: {str(e)}\n"
                                              f"Для возврата в меню воспользуйтесь кнопкой ниже",
                             reply_markup=go_to_menu(), parse_mode='HTML')
            bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)



