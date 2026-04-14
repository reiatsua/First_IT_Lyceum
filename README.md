# 🏫 Экосистема Первого IT-лицея | Основной портал

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-0C4B33?logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)

Центральное звено цифровой инфраструктуры Первого IT-лицея г. Петропавловска. Портал объединяет информационную среду, виртуальную приемную и backend-сервисы для взаимодействия с Telegram-ботами экосистемы.

## 🌟 Ключевые фичи (UI/UX & Tech)
* **Mobile-First Design:** Полностью адаптивный хедер с выездным Offcanvas-меню слева и интуитивной кнопкой профиля (FAB) в нижнем углу для смартфонов.

* **Cloud Media:** Интеграция с Cloudinary API для надежного хранения изображений (новости, аватары, фото педагогов), что решает проблему эфемерной файловой системы в облаке.

* **Production Stack:** Использование WhiteNoise для раздачи статики и поддержка PostgreSQL в качестве основной БД.

* **Interactive Contacts:** Реализована карта с прецизионными координатами лицея и блок соцсетей с официальными SVG-логотипами и hover-эффектами.

Dynamic UI: Умная шапка, которая скрывается при скролле вниз, освобождая место для контента, и возвращается при скролле вверх.

## 🧩 Модули системы (Микросервисы)
Этот репозиторий содержит только основное Django-приложение. Для полноценной работы всей экосистемы необходим параллельный запуск двух Telegram-ботов (зависимости):
1. **Бот для учеников [Ссылка](https://github.com/reiatsua/Student-bot.git)** — выдача расписания и привязка аккаунтов.
2. **Бот приемной комиссии [Ссылка](https://github.com/reiatsua/Virtual-reception-bot.git)** — авторизация администрации для получения уведомлений.

## 🛠 Технологии
* **Backend:** Python 3, Django 4+
* **База данных:** SQLite (локально), PostgresSQL (в облаке)
* **Интеграции:** Telegram API (библиотека `requests`)
* **Окружение:** `python-dotenv`
* **Хранилище** Cloudinary (Media), WhiteNoise (Static)

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

### 4. Зарегистрируйтесь на сайте хранилища (при деплое)Ж

[cloudinary.com](https://cloudinary.com/)

### 5. Настройка переменных окружения
Создайте файл `.env` в корневой папке проекта и добавьте следующие ключи:
```env
ALLOWED_HOST=ваш_домен
BOT_SECRET_KEY=ваш_секретный_ключ_бота
CLOUD_NAME=имя_вашего_аккаунта_в_cloudinary
CLOUDINARY_API_KEY=ваш_api_ключ_в_cloudinary
CLOUDINARY_API_SECRET=ваш_секретный_ключ_в_cloudinary
CSRF_TRUSTED_ORIGIN=ваша_доменная_страница
DATABASE_URL=url_базы_данных
DEBUG=True
DJANGO_SECRET_KEY=ваша_секретная_ключ
RECEPTION_BOT_TOKEN=токен_бота_приемной
```

### 6. Запуск сервера
Примените миграции базы данных и запустите проект:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```
Сайт будет доступен по адресу: http://127.0.0.1:8000/

## 🌍 Деплой
Проект полностью оптимизирован для Railway. При деплое автоматически подтягиваются настройки БД через DATABASE_URL и выполняется сборка статики.