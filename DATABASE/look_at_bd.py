from peewee_config import db, Client, Feedback, Lesson

# with db:
#     client_list = Client.select()
#     print(f'Имеющиеся клиенты:\n')
#     for i_index, i_client in enumerate(client_list):
#         print(f'ID клиента: {i_client.clients_id}\n'
#               f'ID чата клиента: {i_client.clients_chat_id}\n'
#               f'ИМЯ клиента: {i_client.clients_name}\n'
#               f'ФАМИЛИЯ клиента: {i_client.clients_sirname}\n'
#               f'НОМЕРА клиента: {i_client.clients_number}\n'
#               f'ИМЯ ребенка клиента: {i_client.clients_child_name}\n'
#               f'ДР ребенка клиента: {i_client.clients_child_birthday}\n')

# with db:
#     feedback_list = Feedback.select()
#     print(f'Имеющиеся отзывы и предложения:\n')
#     for i_feed in feedback_list:
#         i_feed.delete_instance()

# Feedback.drop_table()
# Feedback.create_table()

with db:
    client = Client.get_or_none(Client.clients_name == "Джеки")
    lessons = client.lessons

    print(f'Имеющиеся уроки:\n')
    for i_les in lessons:
        print(i_les)
#
# broken_lessons = Lesson.select().where(Lesson.client.is_null(False) & ~(Lesson.client << Client.select(Client.clients_id)))
# for lesson in broken_lessons:
#     lesson.delete_instance()