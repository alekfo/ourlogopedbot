from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

def get_contact():
    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"Отправить номер телефона", request_contact=True)
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    return keyboard

def start_registration():
    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"Начать регистрацию")
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    return keyboard

def go_to_menu():
    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"Перейти в основное меню")
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    return keyboard

def main_clients_commands():
    # Создаём объекты кнопок.
    buttons = [
        r"Информация",
        r"Расписание",
        r"Отзывы и предложения"
    ]
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

def main_admin_commands():
    # Создаём объекты кнопок.
    buttons = [
        r"ИНФО о клиентах",
        r"Управление клиентами",
        r"Управление расписанием",
        r"Выгрузка данных"
    ]
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

def schedule_menu():
    # Создаём объекты кнопок.
    buttons = [
        r"Посмотреть расписание",
        r"Добавить расписание",
        r"Изменить расписание"
    ]

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

def downloads_type():
    # Создаём объекты кнопок.
    buttons = [
        r"Данные активных клиентов",
        r"Расписания",
        r"Архивные данные"
    ]

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

