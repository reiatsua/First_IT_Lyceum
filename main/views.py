import os
import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import News, Page, Appeal, BookAnniversary, SiteSettings, Teacher, TeacherCategory

from .forms import AppealForm

def home(request):
    news_list = News.objects.all()
    return render(request, 'home.html', {'news_list': news_list})

def page_detail(request, slug):
    
    if slug == 'mudryj-uchitel':
        return render(request, 'wise_teacher.html')
    elif slug == 'nemnogo-istorii':
        return render(request, 'bit_of_history.html')
    elif slug == 'our-pride':
        return render(request, 'our_pride.html')
    elif slug == 'bibliotechnaya-dokumentaciya':
        return render(request, 'lib_doc.html')
    elif slug == 'books-jubilee':
        books = BookAnniversary.objects.all() # Вытягиваем книги из базы
        return render(request, 'books_jubilee.html', {'books': books})
    elif slug == 'simvolika':
        return render(request, 'symbols_lyceum.html')
    elif slug == 'weather-cancel':
        return render(request, 'weather_cancel.html')
    elif slug == 'teachers':
        teachers = Teacher.objects.all()
        return render(request, 'teachers.html', {'teachers': teachers})
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'page.html', {'page': page})

def virtual_reception(request):
    if request.method == 'POST':
        form = AppealForm(request.POST)
        if form.is_valid():
            appeal = form.save()

            # --- ИНТЕГРАЦИЯ С ТЕЛЕГРАМ (БАЗА ДАННЫХ) ---
            bot_token = settings.RECEPTION_BOT_TOKEN
            
            try:
                # Берем первую запись из настроек (там будет лежать ID)
                site_settings = SiteSettings.objects.first()
                chat_id = site_settings.reception_chat_id if site_settings else None
                
                if bot_token and chat_id:
                    # Формируем красивое сообщение
                    text = (
                        f"Тип: <b>ОБРАЩЕНИЕ К ПРИЕМНОЙ КОМИССИИ</b>\n\n"
                        f"🚨 <b>Новое обращение!</b>\n"
                        f"👤 <b>ФИО:</b> {appeal.name}\n"
                        f"📞 <b>Контакты:</b> {appeal.contact_info}\n"
                        f"📧 <b>Email:</b> {appeal.email}\n\n"
                        f"📝 <b>Текст:</b>\n{appeal.message}"
                    )
                    
                    # Отправка
                    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                    response = requests.post(url, json={
                        "chat_id": chat_id, 
                        "text": text, 
                        "parse_mode": "HTML"
                    })
                    
                    if response.status_code != 200:
                        print(f"Ошибка TG API: {response.text}")

            except Exception as e:
                print(f"Ошибка при получении chat_id из БД или отправке: {e}")
            # ----------------------------------------------

            messages.success(request, 'Ваше обращение успешно отправлено! Мы рассмотрим его в течение одного дня.')
            return redirect('virtual_reception')
    else:
        form = AppealForm()
    
    return render(request, 'virtual_reception.html', {'form': form})

@csrf_exempt
def update_reception_id(request):
    """Сюда бот отправляет ID директрисы после подтверждения телефона"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Сверяем пароль (защита от хакеров)
            # Если в settings.py нет BOT_SECRET_KEY, используем временный пароль
            secret = getattr(settings, 'BOT_SECRET_KEY', 'default_secret_password')
            if data.get('secret_key') != secret:
                return JsonResponse({"error": "Неверный секретный ключ"}, status=403)
                
            # Сохраняем ID в базу
            setting, created = SiteSettings.objects.get_or_create(id=1)
            setting.reception_chat_id = str(data.get('chat_id'))
            setting.save()
            
            return JsonResponse({"status": "success", "message": "ID успешно обновлен"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Разрешен только POST-запрос"}, status=405)

def teachers_list(request):
    categories = TeacherCategory.objects.prefetch_related('teachers').all()
    return render(request, 'teachers.html', {'categories': categories})