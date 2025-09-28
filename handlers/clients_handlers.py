from datetime import datetime
from telebot import TeleBot
from telebot.types import Message
from config import admin_id
from DATABASE.peewee_config import Client, Feedback
from states import reg_states_client
from keyboards.main_keyboards import (
    go_to_menu,
    main_clients_commands)


def reg_clients_handlers(bot: TeleBot):
    """
    Функция для регистрации основных обработчиков клиента
    :param bot: переменная с приложением
    :return: None
    """

    @bot.message_handler(state=reg_states_client.in_any_block, func=lambda message: 'Информация' in message.text)
    def information(message: Message):
        """
        Обработчик состояния при нажатии кнопки "Информация" в основном меню клиента.
        Выдает клиенту на экран основные возможности бота.
        Есть возможность возврата в основное меню.
        Меняет состояние пользователя на reg_states_client.in_menu
        :param message: переменная с приложением
        :return: None
        """

        bot.send_message(message.chat.id,
                         'Этот бот дает возможность:\n\t'
                         '- смотреть и управлять своим расписанием;\n\t'
                         '- получать уведомления о ближайших записях;\n\t'
                         '- отменять и подтверждать предстоящие записи\n\n'
                         'Для улучшения качества работы нашего центра будем рады оставленным отзывам и предложениям💬📧\n'
                         'Отзывы и предложения выможете оставить, перейдя по вкладке <b>Отзывы и предложения</b> в основном меню\n\n'
                         'Для возврата в основное меню нажмите на кнопку <b>Перейти в основное меню</b>',
                         reply_markup=go_to_menu(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)

    @bot.message_handler(state=reg_states_client.in_any_block, func=lambda message: 'Расписание' in message.text)
    def client_schedule(message: Message):
        """
        Обработчки состояния при нажатии на кнопку "Расписание" в основном меню клиента.
        Проверяет, есть ли запланированные занятия у клиента.
        Елси есть - занятия выводит в отсортированном формате.
        Если нет - выводит об этом сообщение.
        Меняет состояние пользователя на reg_states_client.in_menu
        :param message: переменная с приложением
        :return: None
        """

        current_date = datetime.now().date()
        curr_time_list = datetime.now().time().strftime('%H:%M').split(':')
        curr_client = Client.get_or_none(Client.clients_id == message.from_user.id)

        lessons = curr_client.lessons
        active_lessons = [
            i_lesson
            for i_lesson in lessons
            if i_lesson.lesson_date > current_date or (i_lesson.lesson_date == current_date and int(i_lesson.lessons_dict.get(i_lesson.lesson_number).split(':')[0]) >= int(curr_time_list[0]))
        ]
        if not active_lessons:
            bot.send_message(message.chat.id, "У вас нет запланированных занятий", reply_markup=go_to_menu(), parse_mode='HTML')
            bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)
        else:
            sorted_active_lesson = sorted(active_lessons, key=lambda i_lesson: (i_lesson.day_of_week, i_lesson.lesson_number))
            output_str = 'Вот ваше расписание🗓️:\n\n'
            for i_les in sorted_active_lesson:
                output_str += f'{i_les.days_dict.get(i_les.day_of_week, "Неизвестный день")} - {i_les.lessons_dict.get(i_les.lesson_number, "Неизвестное время")}\n'
            bot.send_message(message.chat.id,
                             output_str,
                             reply_markup=go_to_menu(), parse_mode='HTML')
            bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)

    @bot.message_handler(state=reg_states_client.in_any_block,
                         func=lambda message: 'Отзывы и предложения' in message.text)
    def feedback(message: Message):
        """
        Обработчик состояния при нажатии на кнопку "Отзывы и предложения" в основном меню клиента.
        Предлагает пользователю ввести текст с отзывом или предложением.
        Сохраняется возможность вернуться в основное меню.
        Меняет состояние на reg_states_client.get_feedback
        :param message: переменная с приложением
        :return: None
        """
        bot.send_message(message.chat.id,
                         'Отправьте текст с отзывом или предложением💬\nМы рады любой критике и ценим ваше мнение!\n\n'
                         'Если хотите вернуться в меню - нажмите на кнопку <b>Перейти в основное меню</b>',
                         reply_markup=go_to_menu(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_client.get_feedback, message.chat.id)

    @bot.message_handler(state=reg_states_client.get_feedback)
    def feedback(message: Message):
        """
        Обработчик состояния при получении сообщения обратной связи.
        При получении сообщения "Перейти в основное меню" выдает основное меню клиента.
        Иначе благодарит за оставленный комменатрий и предлагает вернуться в основное меню.
        Также отправляет уведомление админу об оставленном отзыве.
        Обрабатывает ошибки
        :param message: переменная с приложением
        :return: None
        """

        if 'Перейти в основное меню' in message.text:
            output_txt = 'Доступные команды: \n\n'
            output_txt += 'Информация❓ - Показать информацию о возможностях бота\n'
            output_txt += 'Расписание🗓️ - Посмотреть свое расписание\n'
            output_txt += 'Отзывы и предложения💾 - Оставить отзыв или предложения\n'
            bot.send_message(message.chat.id, output_txt, reply_markup=main_clients_commands(), parse_mode='HTML')
            bot.set_state(message.from_user.id, reg_states_client.in_any_block, message.chat.id)
        else:
            curr_client = Client.get_or_none(Client.clients_id == message.from_user.id)
            Feedback.create(
                client=f'{curr_client.clients_name} {curr_client.clients_sirname}',
                text=message.text,
                feedback_date=datetime.now()
            )
            bot.send_message(message.chat.id,
                             'Спасибо за оставленный комментарий!💔\nМы очень ценим это!',
                             reply_markup=go_to_menu(), parse_mode='HTML')
            bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)
            try:
                text = message.text
                bot.send_message(admin_id,
                                 f'🎆{curr_client.clients_name} {curr_client.clients_sirname} оставил(-а) новый отзыв:\n\n"{text}"\n',
                                 reply_markup=go_to_menu(), parse_mode='HTML')
            except Exception as e:
                print('Ошибка отправки админу отзыва:', e)

    @bot.callback_query_handler(
        func=lambda callback_query: (
            callback_query.data in ["confirmed", "canceled"]
        )
    )
    def handle_confirmation(callback_query):
        """
        Обработчки нажатия кнопок подтверждения или отмены занятий клиентом.
        При нажатии на кнопку "Подтвержаю" callback_query равен "confirmed" и отсылаются соответсвующие сообщения клиенту в обратном порядке и
        админу.
        При нажатии на кнопку "Отменить занятие" callback_query равен "canceled" и уходят другие сообещения.
        Удаляется клавиатура. Сообщение-напоминание редактируется в зависмости от нажатой кнопки
        :param callback_query: данные по кнопкам "Подтвержаю" и "Отменить занятие"
        :return: None
        """

        user_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        action = callback_query.data
        original_text = callback_query.message.text

        if action == 'confirmed':
            status_text = 'Подтверждено✅'
            reply_text = 'Ждем Вас к назначенному часу!🙋‍♀️'
            admin_message = 'подтвердил(-а) ближайшую запись!🎉'
        else:
            status_text = 'Отменено❌'
            reply_text = 'Спасибо за уведомление! Свяжитесь с преподавателем, чтобы назначить дату нового занятия!☎️'
            admin_message = 'ОТМЕНИЛ(-А) ближайшую запись!😓'

        new_text = f'{original_text}\n\n{status_text}'
        #Редактируем сообщение
        bot.edit_message_text(
            chat_id=user_id,
            message_id=message_id,
            text=new_text,
            reply_markup=None  # Убираем клавиатуру
        )
        # Отправляем сообщение пользователю.
        bot.send_message(
            callback_query.from_user.id,
            reply_text
        )
        # Отправляем сообщение админу.
        curr_client = Client.get_or_none(Client.clients_id == callback_query.from_user.id)
        message_to_admin = f'{curr_client.clients_name} {curr_client.clients_sirname} {admin_message}'
        bot.send_message(
            admin_id,
            message_to_admin,
        )
#=====КОНЕЦ Обработки подтверждения урока=====