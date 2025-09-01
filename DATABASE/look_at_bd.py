from peewee_config import db, Client

with db:
    client_list = Client.select()
    print(f'Имеющиеся клиенты:\n')
    for i_index, i_client in enumerate(client_list):
        print(f'{i_index + 1}:\n{i_client}')