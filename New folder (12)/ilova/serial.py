"""
REJA - Django REST Framework Serializerlari (serial.py).
Mavzular: REST API, Django REST Framework, API.
"""
from rest_framework import serializers
from ilova.model import Vazifa, Eslatma, Toifa, Foydalanuvchi

class ToifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toifa
        fields = ['id', 'nomi', 'rang', 'belgi']


class VazifaSerializer(serializers.ModelSerializer):
    toifa_nomi = serializers.CharField(source='toifa.nomi', read_only=True)

    class Meta:
        model = Vazifa
        fields = [
            'id', 'sarlavha', 'tavsif', 'toifa', 'toifa_nomi',
            'sana', 'vaqt', 'muhimlik', 'bajarildi', 'yaratildi'
        ]
        read_only_fields = ['id', 'yaratildi']


class EslatmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eslatma
        fields = ['id', 'sarlavha', 'matn', 'rang', 'muhim', 'yaratildi']


class FoydalanuvchiSerializer(serializers.ModelSerializer):
    jami = serializers.IntegerField(source='jami_vazifalar', read_only=True)
    bajarilgan = serializers.IntegerField(source='bajarilgan_vazifalar', read_only=True)
    foiz = serializers.IntegerField(source='bajarilish_foizi', read_only=True)

    class Meta:
        model = Foydalanuvchi
        fields = ['id', 'username', 'first_name', 'last_name', 'yosh', 'kasb', 'jami', 'bajarilgan', 'foiz']
