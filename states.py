from telebot.handler_backends import State, StatesGroup

class reg_states_client(StatesGroup):

    registration = State()
    in_menu = State()
    in_dict = State()
    menu = State()

class reg_states_admin(StatesGroup):

    choise = State()
    in_dict = State()
    menu = State()