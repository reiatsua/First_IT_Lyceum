from django.contrib import admin
from .models import News, Page, Appeal, BookAnniversary, TeacherCategory, Teacher

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'email', 'message')

@admin.register(BookAnniversary)
class BookAnniversaryAdmin(admin.ModelAdmin):
    list_display = ('anniversary_years', 'author', 'writing_year')
    search_fields = ('author', 'description')

@admin.register(TeacherCategory)
class TeacherCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',) # Позволяет менять порядок прямо в списке, не заходя внутрь

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'category', 'position', 'order')
    search_fields = ('full_name', 'position')
    list_filter = ('category',)
    list_editable = ('order',)