from peewee_config import db, Week, Lesson, Client
from datetime import datetime
#
# with db:
#     target_date = datetime.strptime("01.09.2025", "%d.%m.%Y").date()
#     a = Week.get(Week.monday_date == target_date)
#     print(a)

# with db:
#     a = Lesson.select()
#     for i in a:
#         print(a.client.clients_child_name)

with db:
    a = Client.get(Client.clients_child_name == 'Егор Королев')
    lesson = a.lessons
    for i in lesson:
        print(i.day_of_week)
        print(i.lesson_number)
#
    # # Удалить ее
    # a.delete_instance()
    # print("Запись удалена")
