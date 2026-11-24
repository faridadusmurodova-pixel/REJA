"""
REJA - Django Admin boshqaruv paneli (admin.py).
Mavzular: Django, Django ORM.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ilova.model import Foydalanuvchi, Vazifa, Toifa, Eslatma, Maqola

@admin.register(Foydalanuvchi)
class FoydalanuvchiAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'yosh', 'kasb', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Shaxsiy ma\'lumotlar', {'fields': ('yosh', 'kasb', 'telegram_id')}),
    )

@admin.register(Vazifa)
class VazifaAdmin(admin.ModelAdmin):
    list_display = ['sarlavha', 'foydalanuvchi', 'toifa', 'sana', 'vaqt', 'muhimlik', 'bajarildi']
    list_filter = ['muhimlik', 'bajarildi', 'sana', 'toifa']
    search_fields = ['sarlavha', 'tavsif', 'foydalanuvchi__username']

@admin.register(Toifa)
class ToifaAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'foydalanuvchi', 'rang', 'belgi']

@admin.register(Eslatma)
class EslatmaAdmin(admin.ModelAdmin):
    list_display = ['sarlavha', 'foydalanuvchi', 'muhim', 'yaratildi']

@admin.register(Maqola)
class MaqolaAdmin(admin.ModelAdmin):
    list_display = ['sarlavha', 'muallif', 'sana']
