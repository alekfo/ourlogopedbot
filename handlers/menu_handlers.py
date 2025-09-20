from telebot import TeleBot
from telebot.types import Message
from states import reg_states_client, reg_states_admin
from keyboards.main_keyboards import (
    main_clients_commands,
    main_admin_commands)

def reg_menu_handlers(bot: TeleBot):
    """
    Функция для регистрации обработчиков меню клиента и админа
    :param bot: переменная с приложением
    :return: None
    """

    @bot.message_handler(state=reg_states_client.in_menu)
    def show_client_cmd(message: Message):
        """
        Обработчик состояния "в меню клиента".
        Выводит на экран описание основных кнопок.
        Отправляет пользователю кнопки с основными режимами для клиента.
        Меняет состояние пользователя на reg_states_client.in_any_block
        :param message: переменная с приложением.
        :return: None
        """

        output_txt = 'Доступные команды: \n\n'
        output_txt += 'Информация❓ - Показать информацию о возможностях бота\n'
        output_txt += 'Расписание🗓️ - Посмотреть свое расписание\n'
        output_txt += 'Отзывы и предложения💾 - Оставить отзыв или предложения\n'

        bot.send_message(message.chat.id, output_txt, reply_markup=main_clients_commands(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_client.in_any_block, message.chat.id)

    @bot.message_handler(state=reg_states_admin.admin_menu)
    def admin_menu(message: Message):
        """
        Обработчик состояния "в меню админа".
        Предлагает админу нажать на одну из предложенных кнопок с основными разделами.
        Меняет состояние пользователя на reg_states_admin.in_any_block
        :param message: переменная с приложением.
        :return: None
        """

        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=main_admin_commands(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_admin.in_any_block, message.chat.id)