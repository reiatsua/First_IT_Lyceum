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
    
class BookAnniversary(models.Model):
    anniversary_years = models.CharField("Лет юбилею", max_length=50, help_text="Например: 100 лет")
    writing_year = models.CharField("Год написания", max_length=50, help_text="Например: 1922 г.")
    author = models.CharField("Автор", max_length=255)
    description = models.TextField("Описание/Список книг")

    class Meta:
        verbose_name = "Книга-юбиляр"
        verbose_name_plural = "Книги-юбиляры"
        ordering = ['-writing_year'] # Будут идти от новых к старым

    def __str__(self):
        return f"{self.author} — {self.anniversary_years}"
    
class SiteSettings(models.Model):
    reception_chat_id = models.CharField("ID чата приемной", max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Настройка сайта"
        verbose_name_plural = "Настройки сайта"
        
    def __str__(self):
        return "Настройки системы"
    
class TeacherCategory(models.Model):
    name = models.CharField("Название категории", max_length=200)
    order = models.PositiveIntegerField("Порядок отображения", default=0, help_text="Чем меньше число, тем выше категория")

    class Meta:
        verbose_name = "Категория учителей"
        verbose_name_plural = "Категории учителей"
        ordering = ['order']

    def __str__(self):
        return self.name

class Teacher(models.Model):
    category = models.ForeignKey(TeacherCategory, on_delete=models.CASCADE, related_name='teachers', verbose_name="Категория")
    full_name = models.CharField("ФИО", max_length=255)
    position = models.CharField("Должность", max_length=255)
    photo = models.ImageField("Фотография", upload_to='teachers/')
    order = models.PositiveIntegerField("Порядок в списке", default=0)

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"
        ordering = ['order']

    def __str__(self):
        return self.full_name