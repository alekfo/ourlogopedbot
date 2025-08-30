from datetime import datetime
from peewee import SqliteDatabase, Model, CharField, IntegerField, AutoField, ForeignKeyField, DateField
import os
from config import db_path

db = SqliteDatabase(db_path)

class BaseModel(Model):
    class Meta:
        database = db

class Client(BaseModel):
    clients_id = IntegerField(primary_key=True)
    clients_name = CharField(null=False)
    clients_sirname = CharField(null=False)
    clients_number = CharField(null=False)
    clients_child_name = CharField(null=False)
    clients_child_birthday = DateField(null=False)
    def __str__(self):
        return ('1. Имя: {name}\n2. Фамилия: {sirname}\n3. Номер телефона: {phone_number}\n'
                '4. ФИО ребенка: {child_name}\n5. Дата рождения ребенка: {child_birthday}\n').format(
            name=self.clients_name,
            sirname=self.clients_sirname,
            phone_number=self.clients_number,
            child_name=self.clients_child_name,
            child_birthday=self.clients_child_birthday
        )

class Schedule(BaseModel):
    request_id = AutoField()
    clients = ForeignKeyField(Client, backref="schdl", null=False)
    day1 = CharField(null=True)
    day2 = CharField(null=True)
    day3 = CharField(null=True)
    day4 = CharField(null=True)

    def __str__(self):
        return ('Расписание {clients_name}:\n'
                '1. {first_day}\n2. {second_day}\n3. {third_day}\n4. {fourth_day}').format(
            first_day=self.day1,
            second_day=self.day2,
            third_day=self.day3,
            fourth_day=self.day4
        )

def create_models():
    """
    Функция для создания таблицы базы данных на основе созданных моделей
    :return: None
    """

    db.create_tables(BaseModel.__subclasses__())