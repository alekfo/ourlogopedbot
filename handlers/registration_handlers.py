from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from DATABASE.peewee_config import Client
from states import reg_states_client
from keyboards.main_keyboards import (
    go_to_menu,
    get_contact)

def reg_registration_handlers(bot: TeleBot):
    """
    Функция для регистрации обработчиков регистрации нового пользователя.
    :param bot: переменная с приложением
    :return: None
    """

    @bot.message_handler(state=reg_states_client.start_registration)
    def start_reg(message: Message):
        """
        Обработчик состояния старта регстрации. Предлагает пользователю отправить Имя, удаляет кнопку старта регистрации.
        Меяет состояние на reg_states_client.getting_name
        :param message: сообщение от пользователя
        :return: None
        """

        bot.send_message(message.chat.id, 'Отлично! Отправьте Ваше имя', reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.from_user.id, reg_states_client.getting_name, message.chat.id)

    @bot.message_handler(state=reg_states_client.getting_name)
    def got_name(message: Message):
        """
        Обработчик состояния после получения имени от пользователя.
        Проверяет корректность введенного имени.
        Записывает во временный словарь данные с полученным именем.
        Предлагает пользователю отправить Фамилию.
        Меняет состояние на reg_states_client.getting_sirname
        :param message: сообщение от пользователя
        :return: None
        """

        if message.text.isalpha():
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['name'] = message.text
            bot.send_message(message.chat.id, 'Спасибо, записал! Теперь пришлите Вашу фамилию')
            bot.set_state(message.from_user.id, reg_states_client.getting_sirname, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Имя должно состоять только из букв. Пришли корректное имя')

    @bot.message_handler(state=reg_states_client.getting_sirname)
    def got_sirname(message: Message):
        """
        Обработчки состояния после получения Фамилии.
        Првоеряет корректность введенной Фамилии.
        Записывает во временный словарь данные с полученной фамилией.
        Предлагает пользователю отправить номер телефона через нажатие кнопки.
        Меняет состояние на reg_states_client.getting_number
        :param message: сообщение от пользователя
        :return: None
        """

        if message.text.isalpha():
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['sirname'] = message.text
            bot.send_message(message.chat.id,
                             'Спасибо, записал! Теперь мне нужен Ваш номер телефона.\n'
                             'Для отправки номера телефона воспользуйтесь кнопкой <b>Отправить номер телефона</b>',
                             reply_markup=get_contact(), parse_mode='HTML'
                             )
            bot.set_state(message.from_user.id, reg_states_client.getting_number, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Фамилия должна состоять <b>только из букв<b>. Пришли корректную фамилию', parse_mode='HTML')

    @bot.message_handler(content_types=['contact'])
    def got_contact(message):
        """
        Обработчик данных типа "contact".
        Записывает во временный словарь данные с полученным номером телефона.
        Удаляет клавиатуру.
        Предлагает пользователю отправить Имя и Фамилию ребенка.
        Меняет состояние на reg_states_client.getting_child_name
        :param message: сообщение от пользователя
        :return: None
        """

        # message.contact - объект с данными контакта
        phone_number = message.contact.phone_number
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['number'] = phone_number
        bot.send_message(
            message.chat.id,
            f"Отлично! Телефон записал\nТеперь пришлите имя и фамилию Вашего ребенка (через пробел)",
            reply_markup=ReplyKeyboardRemove()  # Убираем клавиатуру
        )
        bot.set_state(message.from_user.id, reg_states_client.getting_child_name, message.chat.id)

    @bot.message_handler(state=reg_states_client.getting_number)
    def wrong_number(message: Message):
        """
        Обработчки состояния, когда пользователь прислал номер телефона, не воспользовавшись кнопкой.
        Предлагает пользователю повторно воспользоваться конопкой
        :param message: сообщение от пользователя
        :return: None
        """
        bot.send_message(message.chat.id,
                         'Для отправки номера телефона необходимо воспользоваться кнопкой <b>Отправить номер телефона</b>',
                         reply_markup=get_contact(), parse_mode='HTML'
                         )

    @bot.message_handler(state=reg_states_client.getting_child_name)
    def got_child_name(message: Message):
        """
        Обработчкие состояния после получения имени и фамилии ребенка.
        Проверяет корректность полученных данных.
        Записывает во временный словарь данные с полученными именем и фамилией ребенка.
        Предлагает пользователю отправить дату рождения ребенка в определенном формате.
        Меняет состояние на reg_states_client.getting_child_birthday
        :param message: сообщение от пользователя
        :return: None
        """

        if len(message.text.split()) == 2:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['child_name'] = message.text
            bot.send_message(message.chat.id,
                             'Записал! Теперь пришлите дату рождения Вашего ребенка\n'
                             'Формат даты: DD.MM.YYYY')
            bot.set_state(message.from_user.id, reg_states_client.getting_child_birthday, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Имя и фамилию ребенка необходимо написать через пробел')

    @bot.message_handler(state=reg_states_client.getting_child_birthday)
    def got_child_birthday(message: Message):
        """
        Обработчик состояния после получения даты рождения ребенка.
        Проверяет корректность введенной даты.
        При получении корректной даты записывает данные пользователя в базу данных.
        Предлагет пользователю перейти в основное меню клиента, воспользовавшись кнопкой.
        Меняет состояние пользователя на reg_states_client.in_menu
        :param message: сообщение от пользователя
        :return: None
        """

        format_list = message.text.split('.')
        if len(format_list) == 3 and 0 < int(format_list[0]) <= 31 and 0 < int(format_list[1]) <= 12 and 0 < int(
                format_list[2]):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['child_birthday'] = message.text
                Client.create(
                    clients_id=message.from_user.id,
                    clients_chat_id=message.chat.id,
                    clients_name=data['name'],
                    clients_sirname=data['sirname'],
                    clients_number=data['number'],
                    clients_child_name=data['child_name'],
                    clients_child_birthday=data['child_birthday']
                )
            bot.send_message(message.chat.id,
                             'Поздравляю с успешной регистрацией! Все необходимые данные получены!\n'
                             'Для перехода в меню нажми на кнопку <b>Перейти в основное меню</b>',
                             reply_markup=go_to_menu(), parse_mode='HTML'
                             )
            bot.set_state(message.from_user.id, reg_states_client.in_menu, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Дата рождения должна быть формата DD.MM.YYYY')