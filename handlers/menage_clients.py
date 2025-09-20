from telebot import TeleBot
from telebot.types import Message
from DATABASE.peewee_config import Client, Lesson
from states import reg_states_admin
from keyboards.main_keyboards import go_to_menu

def reg_menage_clients(bot: TeleBot):
    """
    Функция для регистрации обработчиков в режиме управления клиентами (удаление клиентов).
    :param bot: переменная с приложением
    :return: None
    """

    @bot.message_handler(state=reg_states_admin.in_any_block,
                         func=lambda message: 'Управление клиентами' in message.text)
    def clients_info(message: Message):
        """
        Обработчик состояния после нажатия на кнопку "Управление клиентами".
        Предлагает админу прислать Имя и Фамилию клиента для удаления его из базы данных.
        Меняет состояние пользователя на reg_states_admin.delete_client.
        Сохраняется возможность возвращения в основное меню кнопкой "Перейти в основное меню"
        :param message: переменная с приложением
        :return: None
        """

        bot.send_message(message.chat.id,
                        'Пришлите Имя и Фамилию клиента, которого хотите удалить\n\n'
                        'Для возврата в меню нажмите на кнопку <b>Перейти в основное меню</b>',
                        reply_markup=go_to_menu(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states_admin.delete_client, message.chat.id)

    @bot.message_handler(state=reg_states_admin.delete_client)
    def delete_client(message: Message):
        """
        Обработчик состояния после ввода админом имени и фамилии клиента для удаления.
        Проверка корректность введенных данных.
        При получении корректных данных удаляет указанного клиента из базы данных,
        а также удаляет все уроки, связанные с данным клиентом.
        Отправляет в чат админа подтверждение удаления.
        Меняет состояние пользователя на reg_states_admin.admin_menu
        :param message: переменная с приложением
        :return: None
        """

        try:
            try:
                name_sirname = message.text.split()
                client_to_delete = Client.get_or_none(Client.clients_name == name_sirname[0] and Client.clients_sirname == name_sirname[1])
            except Exception as e:
                raise ValueError('некорректный ввод данных\n\nНеобходимо ввести Имя и Фамилию через пробел')
            else:
                if client_to_delete:
                    client_to_delete.delete_instance()
                    #удаляем все уроки в которых был удаленный клиент
                    broken_lessons = Lesson.select().where(
                        Lesson.client.is_null(False) & ~(Lesson.client << Client.select(Client.clients_id)))
                    for lesson in broken_lessons:
                        lesson.delete_instance()
                else:
                    raise ValueError('такого клиента нет в базе данных\n\nВведите корректные данные или вернитесь в основное меню')
        except ValueError as e:
            bot.send_message(message.chat.id,
                             f'При удалении возникла ошибка: {e}',
                             reply_markup=go_to_menu())
        else:
            bot.send_message(message.chat.id,
                             f'✅Клиент <b>{name_sirname[0]} {name_sirname[1]}</b> успешно удален из базы данных\n\n'
                             f'Для просмотра списка активных клиентов пройдите в раздел <b>ИНФО о клиентах</b> в основном меню',
                             reply_markup=go_to_menu(), parse_mode='HTML')
            bot.set_state(message.from_user.id, reg_states_admin.admin_menu, message.chat.id)