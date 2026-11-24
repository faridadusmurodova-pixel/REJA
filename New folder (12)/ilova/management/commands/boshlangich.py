"""
REJA - Boshlang'ich umumiy toifalar va maqolalarni yuklash (boshlangich.py).
Mavzular: Django ORM, QuerySetlar.
"""
from django.core.management.base import BaseCommand
from ilova.model import Toifa, Maqola, Foydalanuvchi

class Command(BaseCommand):
    help = "Boshlang'ich umumiy toifalarni va foydali maqolalarni yaratadi."

    def handle(self, *args, **options):
        self.stdout.write("Boshlang'ich toifalar yuklanmoqda...")

        # 1. Umumiy toifalar
        toifalar_nomlari = [
            ("Ish va Loyihalar", "#10b981", "💼"),
            ("O'qish va Ta'lim", "#7c3aed", "📚"),
            ("Shaxsiy hayot", "#3b82f6", "🏠"),
            ("Salomatlik va Sport", "#ec4899", "🏃"),
            ("Moliya va Reja", "#f59e0b", "💰"),
        ]
        for nomi, rang, belgi in toifalar_nomlari:
            Toifa.objects.get_or_create(
                nomi=nomi,
                defaults={'rang': rang, 'belgi': belgi}
            )

        self.stdout.write(self.style.SUCCESS("Boshlang'ich toifalar muvaffaqiyatli tayyorlandi!"))
