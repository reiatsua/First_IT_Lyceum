from django.db import models
from django.urls import reverse

class News(models.Model):
    title = models.CharField('Заголовок', max_length=250)
    content = models.TextField('Текст новости')
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Page(models.Model):
    title = models.CharField('Название вкладки', max_length=200)
    slug = models.SlugField('URL-адрес (на англ.)', unique=True)
    content = models.TextField('Содержимое страницы', blank=True)
    
    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы меню'

    def __str__(self):
        return self.title

class Appeal(models.Model):
    name = models.CharField('ФИО', max_length=150)
    contact_info = models.CharField('Телефон', max_length=250, default='')
    email = models.EmailField('E-mail')
    message = models.TextField('Ваше заявление')
    created_at = models.DateTimeField('Дата отправки', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Виртуальная приемная'
        ordering = ['-created_at']

    def __str__(self):
        return f"Обращение от {self.name}"