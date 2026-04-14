from django.http import JsonResponse
import os
import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # Берем данные из POST
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email 
            
            user.save()
            login(request, user)
            messages.success(request, 'Добро пожаловать! Регистрация прошла успешно.')
            return redirect('home')
        else:
            # ВАЖНО: Мы НЕ пересоздаем форму. 
            # Мы просто идем дальше, и render ниже вернет форму с ошибками.
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        # Вытаскиваем данные напрямую из запроса (поле в HTML может называться email или username)
        login_input = request.POST.get('email') or request.POST.get('username')
        password_input = request.POST.get('password')

        if login_input and password_input:
            user_obj = None
            
            # Шаг 1: Пытаемся найти пользователя по почте
            try:
                user_obj = CustomUser.objects.get(email=login_input)
            except CustomUser.DoesNotExist:
                # Если по почте не нашли, даем шанс зайти по логину (вдруг кто-то введет admin812)
                try:
                    user_obj = CustomUser.objects.get(username=login_input)
                except CustomUser.DoesNotExist:
                    pass

            # Шаг 2: Если человек найден, проверяем пароль
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password_input)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    # Пользователь есть, но пароль не тот
                    messages.error(request, 'Неверный пароль. Попробуйте еще раз.')
            else:
                # Пользователя с такой почтой нет в базе
                messages.error(request, 'Пользователь с такими данными не найден.')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')

        # Если дошли сюда, значит была ошибка входа. Возвращаем форму обратно.
        form = UserLoginForm(request.POST)
        return render(request, 'users/login.html', {'form': form})
        
    else:
        # Это GET-запрос (просто открыли страницу)
        form = UserLoginForm()
        return render(request, 'users/login.html', {'form': form})

@login_required
def profile_view(request):
    # --- НОВЫЙ БЛОК ДЛЯ ГЕНЕРАЦИИ КОДА ТЕЛЕГРАМ ---
    if request.method == 'POST' and 'generate_tg_code' in request.POST:
        request.user.generate_tg_code()
        # Обрати внимание: если в urls.py путь называется 'profile_view', 
        # то в redirect нужно писать его. Если там name='profile', то оставляй как есть.
        return redirect('profile') 
    # ---------------------------------------------

    # Дальше идет твой стандартный код
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})

@csrf_exempt
def sync_telegram_api(request):
    if request.method == 'POST':
        sync_code = request.POST.get('sync_code')
        chat_id = request.POST.get('chat_id')
        
        try:
            # Ищем пользователя с таким кодом
            user = CustomUser.objects.get(telegram_sync_code=sync_code)
            # Привязываем ID чата
            user.telegram_chat_id = chat_id
            # Очищаем код, чтобы его нельзя было использовать дважды
            user.telegram_sync_code = None 
            user.save()
            
            return JsonResponse({'status': 'success'}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Invalid code'}, status=404)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_schedule_api(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id')
        
        try:
            user = CustomUser.objects.get(telegram_chat_id=chat_id)
            
            # Проверяем, заполнены ли данные ученика
            if not user.grade_number or not user.grade_letter or not user.subgroup:
                return JsonResponse({'error': 'В твоем профиле на сайте не указан класс или подгруппа!'}, status=400)
            
            # Переводим русскую букву из БД (Б) в английскую для файла (B)
            ru_to_en = {'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G'}
            letter_en = ru_to_en.get(user.grade_letter, user.grade_letter)

            # Путь к файлу: BASE_DIR / static / schedule / 10B_1.txt
            file_name = f"{user.grade_number}{letter_en}_{user.subgroup}.txt"
            file_path = os.path.join(settings.BASE_DIR, 'static', 'schedule', file_name)
            
            if not os.path.exists(file_path):
                return JsonResponse({'error': f'Файл расписания для твоего класса ({file_name}) не найден на сервере.'}, status=404)

            # Определяем завтрашний день недели
            today = datetime.datetime.today().weekday()
            tomorrow = (today + 1) % 7
            
            if tomorrow >= 5: # 5 - Суббота, 6 - Воскресенье
                return JsonResponse({'text': 'Завтра выходной! Отдыхай! 🎉'}, status=200)

            markers = ["1️⃣Понедельник:", "2️⃣Вторник:", "3️⃣Среда:", "4️⃣Четверг:", "5️⃣Пятница:"]
            target_marker = markers[tomorrow]

            # Читаем файл
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            schedule_text = ""
            is_recording = False

            for line in lines:
                if target_marker in line:
                    is_recording = True
                    schedule_text += f"📅 <b>Расписание на завтра ({target_marker[:-1]}):</b>\n\n"
                    continue
                
                if is_recording:
                    stripped_line = line.strip()
                    # Если наткнулись на одиночную цифру следующего дня (1, 2, 3...) - останавливаемся
                    if stripped_line in ['1', '2', '3', '4', '5', '6'] and '️⃣' not in stripped_line:
                        break
                    
                    if stripped_line and "10B" not in stripped_line:
                        schedule_text += f"{line.rstrip()}\n"

            if not schedule_text:
                return JsonResponse({'error': 'Не удалось найти расписание на завтра.'}, status=404)

            # Отдаем боту готовый текст
            return JsonResponse({'text': schedule_text}, status=200)

        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Твой Telegram не привязан к сайту. Нажми "Привязать" в профиле!'}, status=404)

    return JsonResponse({'error': 'Method not allowed'}, status=405)