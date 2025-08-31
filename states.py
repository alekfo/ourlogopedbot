from telebot.handler_backends import State, StatesGroup

class reg_states_client(StatesGroup):

    start_registration = State()
    getting_name = State()
    getting_sirname = State()
    getting_number = State()
    getting_child_name = State()
    getting_child_birthday = State()

    in_menu = State()
    in_any_block = State()

class reg_states_admin(StatesGroup):

    admin_menu = State()
    choise_action = State()
    menu = State()