import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import News, Page, Appeal, BookAnniversary
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
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'page.html', {'page': page})

def virtual_reception(request):
    if request.method == 'POST':
        form = AppealForm(request.POST)
        if form.is_valid():
            appeal = form.save()

            # --- ИНТЕГРАЦИЯ С ТЕЛЕГРАМ (ЧИСТЫЙ ВАРИАНТ) ---
            # Берем настройки, которые мы прописали в settings.py
            chat_id_file = settings.RECEPTION_CHAT_ID_FILE
            bot_token = settings.RECEPTION_BOT_TOKEN
            
            # Проверяем: есть ли токен и существует ли файл с ID чата
            if bot_token and chat_id_file and os.path.exists(chat_id_file):
                try:
                    with open(chat_id_file, 'r', encoding="utf-8") as f:
                        chat_id = f.read().strip()
                    
                    if chat_id:
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
                        
                        # Если вдруг телеграм вернул ошибку, увидим в консоли
                        if response.status_code != 200:
                            print(f"Ошибка TG API: {response.text}")

                except Exception as e:
                    print(f"Ошибка при чтении chat_id или отправке: {e}")
            # ----------------------------------------------

            messages.success(request, 'Ваше обращение успешно отправлено! Мы рассмотрим его в течение одного дня.')
            return redirect('virtual_reception')
    else:
        form = AppealForm()
    
    return render(request, 'virtual_reception.html', {'form': form})
