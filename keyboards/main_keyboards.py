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
    button_1 = KeyboardButton(text=r"Информация")
    button_2 = KeyboardButton(text=r"Расписание")
    button_3 = KeyboardButton(text=r"Отзывы и предложения")
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1, button_2, button_3)
    return keyboard

def main_admin_commands():
    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"ИНФО о клиентах")
    button_2 = KeyboardButton(text=r"Управление клиентами")
    button_3 = KeyboardButton(text=r"Управление расписанием")
    button_4 = KeyboardButton(text=r"Выгрузка данных")
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1, button_2, button_3, button_4)
    return keyboard

def schedule_menu():
    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"Посмотреть расписание")
    button_2 = KeyboardButton(text=r"Добавить расписание")
    button_3 = KeyboardButton(text=r"Изменить расписание")
    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1, button_2, button_3)
    return keyboard

