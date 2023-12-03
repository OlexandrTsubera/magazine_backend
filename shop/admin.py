from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'update']
    list_filter = ['available', 'created', 'update']
    list_editable = ['price', 'available']  # Поля які можна буде редагувати в адмін-панелі
    prepopulated_fields = {'slug': ('name',)}  # Вказує на те, що поле slug буде генеруватися за допомогою поля name
    