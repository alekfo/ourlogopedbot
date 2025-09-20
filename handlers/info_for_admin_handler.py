from telebot import TeleBot
from telebot.types import Message
from DATABASE.peewee_config import Client
from states import reg_states_admin
from keyboards.main_keyboards import go_to_menu

def reg_info_about_clients(bot: TeleBot):
    """
    Функция для регистрации обработчика для отправки информации об активных клиентах
    :param bot: переменная с приложением
    :return: None
    """

    @bot.message_handler(state=reg_states_admin.in_any_block,
                         func=lambda message: 'ИНФО о клиентах' in message.text)
    def clients_info(message: Message):
        """
        Обработчик состояния in_any_block при нажатии на кнопку "ИНФО о клиентах".
        Отправляет админу информацию обо всех активных клиентах.
        Меняет состояние пользователя на reg_states_admin.admin_menu
        :param message: переменная с приложением
        :return: None
        """

        output_info = ('Вот вся информация об активных клиентах:\n\n')
        clients = Client.select()
        for i_client in clients:
            output_info += str(i_client)
        bot.send_message(message.chat.id,
                        output_info,
                        reply_markup=go_to_menu(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)