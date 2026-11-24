"""
REJA - Django ModelForm formalari (forma.py).
Mavzular: Django ModelForm, Django ORM.
"""
from django import forms
from ilova.model import Vazifa, Eslatma, Toifa, Foydalanuvchi

class VazifaFormasi(forms.ModelForm):
    """34. Django ModelForm: Vazifa qo'shish va tahrirlash formasi"""
    class Meta:
        model = Vazifa
        fields = ['sarlavha', 'tavsif', 'toifa', 'sana', 'vaqt', 'muhimlik', 'bajarildi']
        widgets = {
            'sarlavha': forms.TextInput(attrs={
                'class': 'shakl-kiritish',
                'placeholder': 'Reja yoki vazifa nomi...'
            }),
            'tavsif': forms.Textarea(attrs={
                'class': 'shakl-kiritish',
                'rows': 3,
                'placeholder': 'Batafsil tavsif (ixtiyoriy)...'
            }),
            'toifa': forms.Select(attrs={'class': 'shakl-tanlash'}),
            'sana': forms.DateInput(attrs={'class': 'shakl-kiritish', 'type': 'date'}),
            'vaqt': forms.TimeInput(attrs={'class': 'shakl-kiritish', 'type': 'time'}),
            'muhimlik': forms.Select(attrs={'class': 'shakl-tanlash'}),
            'bajarildi': forms.CheckboxInput(attrs={'class': 'shakl-belgi'}),
        }

    def __init__(self, *args, foydalanuvchi=None, **kwargs):
        super().__init__(*args, **kwargs)
        if foydalanuvchi:
            # Faqat o'sha foydalanuvchining o'z toifalarini ko'rsatish (Izolyatsiya)
            self.fields['toifa'].queryset = Toifa.objects.filter(
                models_q := (forms.models.Q(foydalanuvchi=foydalanuvchi) | forms.models.Q(foydalanuvchi__isnull=True))
            )


class EslatmaFormasi(forms.ModelForm):
    """Eslatma yaratish formasi"""
    class Meta:
        model = Eslatma
        fields = ['sarlavha', 'matn', 'rang', 'muhim']
        widgets = {
            'sarlavha': forms.TextInput(attrs={'class': 'shakl-kiritish', 'placeholder': 'Eslatma sarlavhasi...'}),
            'matn': forms.Textarea(attrs={'class': 'shakl-kiritish', 'rows': 4, 'placeholder': 'Eslatma matni...'}),
            'rang': forms.TextInput(attrs={'class': 'shakl-kiritish', 'type': 'color'}),
            'muhim': forms.CheckboxInput(attrs={'class': 'shakl-belgi'}),
        }


class ProfilFormasi(forms.ModelForm):
    """Profilni tahrirlash formasi"""
    class Meta:
        model = Foydalanuvchi
        fields = ['first_name', 'last_name', 'yosh', 'kasb', 'telegram_id']
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'yosh': 'Yosh',
            'kasb': 'Kasb / Yo‘nalish',
            'telegram_id': 'Telegram ID',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'shakl-kiritish'}),
            'last_name': forms.TextInput(attrs={'class': 'shakl-kiritish'}),
            'yosh': forms.NumberInput(attrs={'class': 'shakl-kiritish'}),
            'kasb': forms.TextInput(attrs={'class': 'shakl-kiritish'}),
            'telegram_id': forms.TextInput(attrs={'class': 'shakl-kiritish'}),
        }
