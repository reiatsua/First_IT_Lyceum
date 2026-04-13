import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Ученик'),
        ('teacher', 'Учитель'),
        ('parent', 'Родитель'),
    )
    
    email = models.EmailField('Почта', unique=True)
    patronymic = models.CharField('Отчество', max_length=50, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=20)
    role = models.CharField('Роль', max_length=10, choices=ROLE_CHOICES)
    iin = models.CharField('ИИН', max_length=12, blank=True, null=True)
    avatar = models.ImageField('Аватарка', upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    telegram_chat_id = models.CharField('ID Telegram', max_length=100, blank=True, null=True)
    telegram_sync_code = models.CharField('Код синхронизации', max_length=10, blank=True, null=True)

    GRADE_CHOICES = [(i, str(i)) for i in range(1, 12)] # Список от 1 до 11
    LETTER_CHOICES = [('А', 'А'), ('Б', 'Б'), ('В', 'В'), ('Г', 'Г')]
    SUBGROUP_CHOICES = [(1, '1'), (2, '2')]

    grade_number = models.IntegerField('Класс', choices=GRADE_CHOICES, blank=True, null=True)
    grade_letter = models.CharField('Буква', max_length=1, choices=LETTER_CHOICES, blank=True, null=True)
    subgroup = models.IntegerField('Подгруппа', choices=SUBGROUP_CHOICES, blank=True, null=True)

    def generate_tg_code(self):
        """Генерирует случайный 6-значный код из цифр для привязки бота"""
        code = ''.join(random.choices(string.digits, k=6))
        self.telegram_sync_code = code
        self.save()
        return code

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.get_role_display()})"