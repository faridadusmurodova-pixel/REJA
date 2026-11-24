"""
REJA - Ma'lumotlar bazasi modellari (model.py).
Mavzular: Django ORM, QuerySetlar, OOP, Database so'rovlari, Blog sayt.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Foydalanuvchi(AbstractUser):
    """
    Shaxsiy hisob foydalanuvchisi.
    Ism, familiya va yosh har bir shaxs uchun alohida saqlanadi.
    """
    yosh = models.PositiveIntegerField(default=20, verbose_name="Yosh")
    kasb = models.CharField(max_length=100, default="Dasturchi", blank=True, verbose_name="Kasb")
    telegram_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telegram ID")

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    @property
    def ism(self):
        return self.first_name if self.first_name else self.username

    @property
    def familiya(self):
        return self.last_name

    @property
    def toliq_ism(self):
        matn = f"{self.first_name} {self.last_name}".strip()
        return matn if matn else self.username

    def jami_vazifalar(self):
        return self.vazifalar.count()

    def bajarilgan_vazifalar(self):
        return self.vazifalar.filter(bajarildi=True).count()

    def bajarilmagan_vazifalar(self):
        return self.vazifalar.filter(bajarildi=False).count()

    def bugungi_vazifalar(self):
        bugun = timezone.now().date()
        return self.vazifalar.filter(sana=bugun).count()

    def bajarilish_foizi(self):
        jami = self.jami_vazifalar()
        if jami == 0:
            return 0
        bajarilgan = self.bajarilgan_vazifalar()
        return int((bajarilgan / jami) * 100)

    # Qisqa laqablar (alias)
    def jami(self):
        return self.jami_vazifalar()

    def bajarilgan(self):
        return self.bajarilgan_vazifalar()

    def bajarilmagan(self):
        return self.bajarilmagan_vazifalar()

    def kutilayotgan(self):
        return self.bajarilmagan_vazifalar()

    def kutilayotgan_vazifalar_soni(self):
        return self.bajarilmagan_vazifalar()

    def bugun(self):
        return self.bugungi_vazifalar()

    def foiz(self):
        return self.bajarilish_foizi()

    def __str__(self):
        return f"{self.toliq_ism} ({self.yosh} yosh)"


class Toifa(models.Model):
    """Vazifa toifasi (Masalan: Ish, O'qish, Shaxsiy, Sport)"""
    foydalanuvchi = models.ForeignKey(
        Foydalanuvchi, on_delete=models.CASCADE, related_name='toifalar',
        null=True, blank=True
    )
    nomi = models.CharField(max_length=50, verbose_name="Toifa nomi")
    rang = models.CharField(max_length=20, default="#10b981", verbose_name="Rang kodi")
    belgi = models.CharField(max_length=10, default="📌", verbose_name="Belgi")

    class Meta:
        verbose_name = "Toifa"
        verbose_name_plural = "Toifalar"

    def __str__(self):
        return f"{self.belgi} {self.nomi}"


class Vazifa(models.Model):
    """
    Shaxsiy reja / vazifa modeli.
    Foydalanuvchiga qat'iy bog'langan (izolyatsiya qilingan).
    """
    MUHIMLIK_DARAJASI = [
        ('past', 'Past'),
        ('orta', "O'rta"),
        ('yuqori', 'Yuqori'),
    ]

    foydalanuvchi = models.ForeignKey(
        Foydalanuvchi, on_delete=models.CASCADE, related_name='vazifalar',
        verbose_name="Egasi"
    )
    toifa = models.ForeignKey(
        Toifa, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='vazifalar', verbose_name="Toifa"
    )
    sarlavha = models.CharField(max_length=200, verbose_name="Reja / Vazifa nomi")
    tavsif = models.TextField(blank=True, verbose_name="Tavsif")
    sana = models.DateField(default=timezone.now, verbose_name="Sana")
    vaqt = models.TimeField(blank=True, null=True, verbose_name="Vaqt")
    muhimlik = models.CharField(max_length=20, choices=MUHIMLIK_DARAJASI, default='orta', verbose_name="Muhimlik")
    bajarildi = models.BooleanField(default=False, verbose_name="Bajarildi")
    yaratildi = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Vazifa"
        verbose_name_plural = "Vazifalar"
        ordering = ['bajarildi', 'sana', 'vaqt', '-yaratildi']

    @property
    def muddat(self):
        return self.sana

    @muddat.setter
    def muddat(self, qiymat):
        self.sana = qiymat

    def __str__(self):
        holat = "✓" if self.bajarildi else "○"
        return f"[{holat}] {self.sarlavha}"

# Reja nomi bilan ham chaqirish imkoniyati
Reja = Vazifa


class Eslatma(models.Model):
    """Foydalanuvchining shaxsiy eslatmalari"""
    foydalanuvchi = models.ForeignKey(
        Foydalanuvchi, on_delete=models.CASCADE, related_name='eslatmalar'
    )
    sarlavha = models.CharField(max_length=150, verbose_name="Sarlavha")
    matn = models.TextField(verbose_name="Eslatma matni")
    rang = models.CharField(max_length=20, default="#1e1035", verbose_name="Rang")
    muhim = models.BooleanField(default=False, verbose_name="Muhim eslatma")
    yaratildi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Eslatma"
        verbose_name_plural = "Eslatmalar"
        ordering = ['-muhim', '-yaratildi']

    def __str__(self):
        return self.sarlavha


class Maqola(models.Model):
    """
    Blog sahifasi uchun foydali maqolalar (Blog sayt mavzusi uchun).
    Masalan: Vaqtni to'g'ri boshqarish, Pomodoro usuli, Soft Skills.
    """
    muallif = models.ForeignKey(
        Foydalanuvchi, on_delete=models.CASCADE, related_name='maqolalar'
    )
    sarlavha = models.CharField(max_length=200, verbose_name="Maqola sarlavhasi")
    matn = models.TextField(verbose_name="Maqola matni")
    sana = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Maqola"
        verbose_name_plural = "Maqolalar"

    def __str__(self):
        return self.sarlavha
