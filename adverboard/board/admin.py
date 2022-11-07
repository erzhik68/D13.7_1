from django.contrib import admin
from .models import Ad, Category, Comment, Image

'''
Встроенный редактор создает на странице добавления или правки записи первичной
модели НАБОР ФОРМ для работы со связанными записями вторичной модели
Класс встроенного редактора должен быть производным от одного из следующих
классов, объявленных в модуле django.contrib.admin
Stackediniine — элементы управления располагаются по вертикали
Tabuiariniine — элементы управления располагаются по горизонтали. Для формирования
набора форм применяется таблица HTML.
'''
class ImageInLine(admin.TabularInline):
    model = Image
    extra = 1

@admin.register((Ad))
class AdAdmin(admin.ModelAdmin):
    inlines = [ImageInLine]

# admin.site.register(Ad)
admin.site.register(Category)
# admin.site.register(Image)
admin.site.register(Comment)