from django.contrib import admin
from .models import News, Page, Appeal, BookAnniversary

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    # Убрали 'subject', добавили 'name' и 'email'
    list_display = ('name', 'email', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    # В поиске тоже заменили 'subject' на 'email'
    search_fields = ('name', 'email', 'message')

@admin.register(BookAnniversary)
class BookAnniversaryAdmin(admin.ModelAdmin):
    list_display = ('anniversary_years', 'author', 'writing_year')
    search_fields = ('author', 'description')