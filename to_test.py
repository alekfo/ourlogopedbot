from datetime import datetime, timedelta
from DATABASE.peewee_config import Client, Week, Lesson
import time
#
# lessons_dict = {
#         1: '8:00',
#         2: '8:45',
#         3: '9:30',
#         4: '10:15',
#         5: '11:00',
#         6: '11:45',
#         7: '12:30',
#         8: '13:15',
#         9: '17:30',
#         10: '18:15',
#         11: '19:00',
#     }
#
# now = datetime.now()
#
# target_time = now + timedelta(hours=9)
# a = target_time.time().strftime('%H:%M').split(':')
#
#
# print(now)
# print(target_time)
#
# print(target_time.date())
# print(a)

now = datetime.now()
target_time = now + timedelta(hours=2)
formated_target_time = target_time.time().strftime('%H:%M')

upcoming_lessons = Lesson.select().where(Lesson.lesson_date == target_time.date())

for i_lesson in upcoming_lessons:
        print('ЗАШЕЛ В ЦИКЛ')
        lesson_time = i_lesson.lessons_dict.get(i_lesson.lesson_number, None)
        diff_time = int(lesson_time.split(':')[0]) - int(formated_target_time.split(':')[0])
        if 0 <= diff_time <= 1:
                print(i_lesson.client.clients_name)

time.sleep(1800)