from DATABASE.peewee_config import Client, Week, Lesson
from keyboards.main_keyboards import confirmation_markup
from datetime import datetime, timedelta
import time
from telebot import TeleBot
from config import admin_id

def check_upcoming_lessons(bot: TeleBot):
    while True:
        try:
            now_moscow = datetime.now()
            target_time = now_moscow + timedelta(hours=5)
            formated_target_time = target_time.time().strftime('%H:%M')

            upcoming_lessons = Lesson.select().where(
                Lesson.lesson_date == target_time.date()
            )

            for i_lesson in upcoming_lessons:
                if i_lesson.confirm_flag:
                    continue
                lesson_time = i_lesson.lessons_dict.get(i_lesson.lesson_number, None)
                diff_time = int(lesson_time.split(':')[0]) - int(formated_target_time.split(':')[0])
                if 0 <= diff_time <= 1:
                    # Отправляем уведомление
                    message = (
                        f"🔔 Напоминание!\n\n"
                        f"Приближается занятие:\n"
                        f"📅 Дата: {i_lesson.lesson_date.strftime('%d.%m.%Y')}\n"
                        f"⏰ Время: {lesson_time}\n"
                        f"👤 Кто записан: {i_lesson.client.clients_child_name}"
                    )
                    try:
                        bot.send_message(
                            i_lesson.client.clients_chat_id,
                            message,
                            reply_markup=confirmation_markup()
                        )
                        i_lesson.confirm_flag = True
                        i_lesson.save()
                        print(f"Отправлено напоминание клиенту {i_lesson.client.clients_name}")
                    except Exception as e:
                        bot.send_message(admin_id,
                                         f'Произошла ошибка при отправке уведомления пользователю - '
                                         f'{i_lesson.client.clients_name} {i_lesson.client.clients_sirname}: {e}')

            time.sleep(60)

        except Exception as e:
            bot.send_message(admin_id,
                             f'Произошла ошибка в цикле оповещения: {e}')
            time.sleep(300)  # Ждем 5 минут при ошибке
