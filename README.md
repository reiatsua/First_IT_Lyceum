# 🏫 Экосистема Первого IT-лицея | Основной портал

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-0C4B33?logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)

Основной веб-портал и backend-ядро цифровой экосистемы Первого IT-лицея. Проект включает в себя сайт с новостями, информацией о школе, систему виртуальной приемной и API для взаимодействия с Telegram-ботами.

## 🧩 Модули системы (Микросервисы)
Этот репозиторий содержит только основное Django-приложение. Для полноценной работы всей экосистемы необходим параллельный запуск двух Telegram-ботов (зависимости):
1. **Бот для учеников [Ссылка](https://github.com/reiatsua/Student-bot.git)** — выдача расписания и привязка аккаунтов.
2. **Бот приемной комиссии [Ссылка](https://github.com/reiatsua/Virtual-reception-bot.git)** — авторизация администрации для получения уведомлений.

## 🛠 Технологии
* **Backend:** Python 3, Django 4+
* **База данных:** SQLite (локально)
* **Интеграции:** Telegram API (библиотека `requests`)
* **Окружение:** `python-dotenv`

## 🚀 Как запустить локально

### 1. Подготовка
Склонируйте репозиторий на свой компьютер и перейдите в папку проекта (для корректной работы назовите ее `flyceum`):
```bash
git clone https://github.com/reiatsua/First_IT_Lyceum.git
cd flyceum
```

### 2. Виртуальное окружение
Создайте и активируйте виртуальное окружение:

Для Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Для Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

Примечание: при ошибке выполнения на Windows попробуйте следующую команду:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Установка зависимостей
Установите необходимые библиотеки:
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
Создайте файл `.env` в корневой папке проекта и добавьте следующие ключи:
```env
DJANGO_SECRET_KEY=ваш_секретный_ключ_django
DEBUG=True
RECEPTION_BOT_TOKEN=токен_бота_приемной_комиссии
RECEPTION_FILE_PATH=../reception_bot/admin_chat_id.txt
```

### 5. Запуск сервера
Примените миграции базы данных и запустите проект:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Сайт будет доступен по адресу: http://127.0.0.1:8000/