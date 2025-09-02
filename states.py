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
    in_any_block = State()
    in_schedule = State()
    process_file = State()
    show_schedule = State()
    in_downloads = State()
    in_downloads_schedule = State()