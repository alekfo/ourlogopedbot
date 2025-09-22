from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_contact():
    """
    Функция дял создания объекта клавиатуры с кнопкой для отправки номера телефона
    :return: keyboard
    """

    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"📱Отправить номер телефона", request_contact=True)
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    return keyboard

def start_registration():
    """
    Функция дял создания объекта клавиатуры с кнопкой начала регистрации
    :return: keyboard
    :return:
    """

    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"📝Начать регистрацию")
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    return keyboard

def go_to_menu():
    """
    Функция дял создания объекта клавиатуры с кнопкой для перехода в основное меню
    :return: keyboard
    """

    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"🚀Перейти в основное меню")
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    return keyboard

def main_clients_commands():
    """
    Функция дял создания объекта клавиатуры с кнопками основного меню клиента
    :return: keyboard
    """

    # Создаём объекты кнопок.
    buttons = [
        r"ℹ️Информация",
        r"📅Расписание",
        r"💬Отзывы и предложения"
    ]
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

def main_admin_commands():
    """
    Функция дял создания объекта клавиатуры с кнопками основного меню админа
    :return: keyboard
    """

    # Создаём объекты кнопок.
    buttons = [
        r"👥ИНФО о клиентах",
        r"⚙️Управление клиентами",
        r"🕐Управление расписанием",
        r"📊Выгрузка данных",
        r"📢Сделать рассылку"
    ]
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

def schedule_menu():
    """
    Функция дял создания объекта клавиатуры с кнопками меню действий над расписанием
    :return: keyboard
    """

    # Создаём объекты кнопок.
    buttons = [
        r"👀Посмотреть расписание",
        r"➕Добавить расписание",
        r"✏️Изменить расписание",
        r"🚀Перейти в основное меню"
    ]

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

def downloads_type():
    """
    Функция дял создания объекта клавиатуры с кнопками меню выгрузки данных
    :return: keyboard
    """

    # Создаём объекты кнопок.
    buttons = [
        r"✅Данные активных клиентов",
        r"📅Расписания",
        r"📦Архивные данные",
        r"🚀Перейти в основное меню"
    ]

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

def confirmation_markup():
    """
    Функция дял создания объекта клавиатуры с кнопками подтверждения или отмены приближающегося занятия
    :return: keyboard
    """

    # Создаём объекты кнопок.
    button_1 = InlineKeyboardButton(text="Подтвержаю", callback_data="confirmed")
    button_2 = InlineKeyboardButton(text="Отменить занятие", callback_data="canceled")

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_1, button_2)
    return keyboard

def choise_action():
    """
    Функция дял создания объекта клавиатуры с кнопками меню действий над уроком
    :return: keyboard
    """

    # Создаём объекты кнопок.
    buttons = [
        r"❌Удалить урок",
        r"➕Добавить урок",
        r"🚀Перейти в основное меню"
    ]

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

def lessons_markup():
    """
    Функция дял создания объекта клавиатуры с кнопками доступных уроков
    :return: keyboard
    """

    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r'🕗8:00')
    button_2 = KeyboardButton(text=r'🕗8:45')
    button_3 = KeyboardButton(text=r'🕗9:30')
    button_4 = KeyboardButton(text=r'🕗10:15')
    button_5 = KeyboardButton(text=r'🕗11:00')
    button_6 = KeyboardButton(text=r'🕗11:45')
    button_7 = KeyboardButton(text=r'🕗12:30')
    button_8 = KeyboardButton(text=r'🕗13:15')
    button_9 = KeyboardButton(text=r'🕗17:30')
    button_10 = KeyboardButton(text=r'🕗18:15')
    button_11 = KeyboardButton(text=r'🕗19:00')
    button_12 = KeyboardButton(text=r'🚀Перейти в основное меню')


    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1,
                 button_2,
                 button_3,
                 button_4,
                 button_5,
                 button_6,
                 button_7,
                 button_8,
                 button_9,
                 button_10,
                 button_11,
                 button_12)
    return keyboard

def confirmation_in_schedule():
    """
    Функция дял создания объекта клавиатуры с кнопкой подтверждения удаления урока
    :return: keyboard
    """

    # Создаём объекты кнопок.
    buttons = [
        r"✅Подтверждаю",
        r"🚀Перейти в основное меню"
    ]

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

def days_markup():
    """
    Функция дял создания объекта клавиатуры с кнопками с днями недели
    :return: keyboard
    """

    # Создаём объекты кнопок.
    buttons = [
        r"📆Понедельник",
        r"📆Вторник",
        r"📆Среда",
        r"📆Четверг",
        r"📆Пятница",
        r"📆Суббота"
    ]

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

