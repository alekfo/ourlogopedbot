from datetime import datetime
from peewee import *
import os
from config import db_path
import datetime

db = SqliteDatabase(db_path)

class BaseModel(Model):
    class Meta:
        database = db

class Client(BaseModel):
    clients_id = IntegerField(primary_key=True)
    clients_chat_id = IntegerField(null=False)
    clients_name = CharField(null=False)
    clients_sirname = CharField(null=False)
    clients_number = CharField(null=False)
    clients_child_name = CharField(null=False)
    clients_child_birthday = DateField(null=False)
    def __str__(self):
        return ('Имя: {name}\nФамилия: {sirname}\nНомер телефона: {phone_number}\n'
                'ФИО ребенка: {child_name}\nДата рождения ребенка: {child_birthday}\n').format(
            name=self.clients_name,
            sirname=self.clients_sirname,
            phone_number=self.clients_number,
            child_name=self.clients_child_name,
            child_birthday=self.clients_child_birthday
        )

class Week(BaseModel):
    schedule_id = AutoField(primary_key=True)
    monday_date = DateField(unique=True)

    def __str__(self):
        return str(self.monday_date)

class Lesson(BaseModel):
    days_dict = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота'
    }

    lessons_dict = {
        1: '8:00',
        2: '8:45',
        3: '9:30',
        4: '10:15',
        5: '11:00',
        6: '11:45',
        7: '12:30',
        8: '13:15',
        9: '17:30',
        10: '18:15',
        11: '19:00',
    }

    lesson_id = AutoField(primary_key=True)
    lesson_date = DateField(null=False)
    confirm_flag = BooleanField(default=False)
    # Когда расписание удаляется, удаляются все связанные с ним уроки (CASCADE).
    weekly_schedule = ForeignKeyField(Week, backref='lessons', on_delete='CASCADE')
    # Если клиент удаляется, можно либо установить NULL, либо запретить удаление.
    # RESTRICT или PROTECT не даст удалить клиента, если у него есть записи.
    client = ForeignKeyField(Client, backref='lessons', on_delete='RESTRICT', null=True)
    day_of_week = IntegerField(constraints=[Check('day_of_week >= 0 AND day_of_week <= 5')])
    lesson_number = IntegerField(constraints=[Check('lesson_number >= 1 AND lesson_number <= 11')])

    def __str__(self):
        return ('{day} ({date}):\n    {lesson} - {client}\n'.format(
            day=self.days_dict.get(self.day_of_week, 'Неизвестный день'),
            date=self.lesson_date,
            lesson=self.lessons_dict.get(self.lesson_number, 'Неизвестное время'),
            client=self.client.clients_child_name if self.client else 'Свободно'
        ))

    class Meta:
        # Один слот в расписании (день + номер урока) может быть занят только одним уроком в рамках одного недельного расписания.
        indexes = (
            (('weekly_schedule', 'day_of_week', 'lesson_number'), True),
        )
        database = db


    # def __str__(self):
    #     return ('Расписание {clients_name}:\n'
    #             '1. {first_day}\n2. {second_day}\n3. {third_day}\n4. {fourth_day}').format(
    #         first_day=self.day1,
    #         second_day=self.day2,
    #         third_day=self.day3,
    #         fourth_day=self.day4
    #     )

def create_models():
    """
    Функция для создания таблицы базы данных на основе созданных моделей
    :return: None
    """

    # Подключаемся, если не подключены
    if db.is_closed():
        db.connect()

    db.create_tables(BaseModel.__subclasses__())