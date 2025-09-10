from peewee_config import db, Client, Feedback

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
#     for i_index, i_feed in enumerate(feedback_list):
#         print(i_feed)