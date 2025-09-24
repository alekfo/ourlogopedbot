# Название прокта
Чат-бот "ЛОГОПЕДиЯ"
👨‍👩‍👧‍👦 Telegram-bot: @OURLogopedBot

 [Свяжитесь с нашим ботом:](https://t.me/OURLogopedBot)

 Ссылка на репозиторий: https://github.com/alekfo/ourlogopedbot.git

# Описание прокта
Данный чат-бот дает возможность управления процессом организации занятий в центре "ЛОГОПЕДия"

# Возможности

-  👤Регистрация пользователей
-  🔄2 режима работы бота:
  - режим "Для администратора"
  - режим "Для клиента"
- 👨‍👩‍👧в режиме "Для клиента":
  - просмотр предстоящих уроков;
  - просмотр информации о чат-боте;
  - оставить отзывы и предложения
  - уведомление о предстоящих занятиях
  - уведомление об изменении расписания
  - подтверждение явки на предстоящее занятие или уведомление об отмене занятия
- 👑в режиме "Для администратора":
  - загрузка недельного расписания, сформированного в Exsel-файле
  - изменение активного расписания
  - просотр имеющихся активных клиентов
  - просмотр расписания выбранной недели
  - удаление клиентов
  - хранение информации
  - массовая рассылка уведомлений
  - выгрузка Exsel-отчетности
- 💾хранение данных

# Основные технологии
## Python
```
Использумые библиотеки в файле requirements.txt
База данных: ORM Peewee
```

## Docker
Сборка образа и запуск контейнера описаны ниже

# Установка и запуск

### Клонирование репозитория
```markdown
bash
git clone https://gitlab.skillbox.ru/aleksei_shlenskov/ourlogopedbot.git
cd ourlogopedbot
```

### Установка зависимостей
```markdown
bash
pip install -r requirements.txt
```

### Настройка переменных окружения
Создайте файл .env по существующему шаблону .env.template и добавьте:

```
BOT_TOKEN=YOUR_BOT_TOKEN
ADMIN_ID=YOUR_ADMIN_ID
DATABASE_PATH=YOUR_DATABASE_PATH
```

### Запуск проекта через консоль
```markdown
bash
cd ourlogopedbot
python main.py
```

### Сборка контейнера Docker
В проекте уже собраны Dockerfile и docker-compose.yml. Для сборки образа docker и запуска контейнера необходимо указать путь до файла с базой данных
на вашем локальном устройстве заменив строку '- "/home/vboxuser/PycharmProjects/ourlogopedbot/DATABASE:/app/data"' на ваш путь.
Для сборки образа и запуска контейнера:
```
bash
cd ourlogopedbot
docker compose up -d
```

# Использование

### Основные команды
Для запуска диfлога с ботом достаточно отправить любое сообщение и следовать инструкциям от бота

### Пример использования:
1. [Регистрация клиента](screenshots\registration.png)
2. [Основное меню клиента](screenshots\main_clients_menu.png)
3. [Основное меню администратора](screenshots\main_admins_menu.png)
4. [Раздел основной информации для клиента](screenshots\about_bot_for_client.png)
5. [Вывод информации с расписанием клиента](screenshots\clients_schedule.png)
6. [Оставить отзыв](screenshots\leave_feedback.png)
7. [Вывод информации об активных клиентах в базе данных](screenshots\clients_output.png)
8. [Меню управления расписанием](screenshots\schedule_menu.png)
9. [Вывод расписания выбранной недели](screenshots\show_schedule.png)
10. [Загрузка Exsel-файла с расписанием](screenshots\upload_schedule.png)
11. [Пример Exsel-файла с расписанием](screenshots\exsel_example.png)
11. [Раздел изменения расписания](screenshots\chenge_sched_menu.png)
12. [Удаление урока](screenshots\removing_lesson.png)
13. [Добавление урока](screenshots\adding_lesson.png)
14. [Раздел выгрузки данных](screenshots\downloads.png)
15. [Массовая рассылка активным клиентам](screenshots\mass_mailing.png)
16. [Уведомление о предстоящем занятии](screenshots\notifications_about_upcoming_lessons.png)
17. [Уведомление об изменении расписания клиента](screenshots\notifications_about_changes.png)
18. [Уведомление админа об подтверждении/отмене занятия](screenshots\confirmation_or_cancelation.png)

# Автор
Шленсков Алексей



