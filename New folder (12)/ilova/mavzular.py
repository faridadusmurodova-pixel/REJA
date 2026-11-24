"""
REJA - 41 ta mavzuning sodda va tushunarli amaliy ifodasi (mavzular.py).
Har bir mavzu oddiy dasturchi tushunadigan uslubda yozilgan va tizimda qo'llaniladi.
"""
import copy
import functools
import sqlite3
import time
from pathlib import Path
from django.db import transaction
from django.conf import settings

# 1. STRING
def matnni_tozala(matn: str) -> str:
    """String metodlari: strip, capitalize, title"""
    if not matn:
        return ""
    toza = matn.strip()
    return toza.capitalize()

# 2. LIST
def vazifalar_royxatini_tartibla(royxat: list) -> list:
    """List metodlari: nusxalash va saralash"""
    yangi_royxat = list(royxat)
    yangi_royxat.sort(key=lambda x: getattr(x, 'sana', None) or '')
    return yangi_royxat

# 3. SHART OPERATORLARI
def muhimlik_rangi(muhimlik: str) -> str:
    """if, elif, else orqali shart tekshirish"""
    if muhimlik == 'yuqori':
        return '#ef4444'  # Qizil
    elif muhimlik == 'orta':
        return '#f59e0b'  # Sariq
    else:
        return '#10b981'  # Yashil

# 4. MANTIQIY OPERATORLAR
def shoshilinchmi(muhimlik: str, bajarildi: bool) -> bool:
    """and, or, not mantiqiy operatorlari"""
    return (muhimlik == 'yuqori' or muhimlik == 'orta') and not bajarildi

# 5. FOR SIKLI
def jami_harflar_soni(vazifalar) -> int:
    """For sikli orqali sarlavhalardagi belgilar sonini hisoblash"""
    jami = 0
    for v in vazifalar:
        jami += len(v.sarlavha)
    return jami

# 6. WHILE SIKLI
def orqaga_sanash(boshlangich: int = 3) -> list:
    """While sikli orqali qadamlarni hisoblash"""
    natija = []
    son = boshlangich
    while son > 0:
        natija.append(son)
        son -= 1
    return natija

# 7. FUNKSIYA
def foiz_hisobla(qism: int, butun: int) -> int:
    """Oddiy va sof funksiya"""
    if butun <= 0:
        return 0
    return int((qism / butun) * 100)

# 8. COPY
def reja_shablonini_nusxala(shablon: dict) -> dict:
    """copy.copy - yengil nusxa olish"""
    return copy.copy(shablon)

# 9. DEEPCOPY
def toliq_reja_nusxasi(malumot: dict) -> dict:
    """copy.deepcopy - chuqur va to'liq nusxa olish"""
    return copy.deepcopy(malumot)

# 10. DICTIONARY
def hisobot_lugati(jami: int, bajarildi: int, kutilmoqda: int) -> dict:
    """Lug'at (dict) tuzilmasi bilan ishlash"""
    return {
        'jami': jami,
        'bajarildi': bajarildi,
        'kutilmoqda': kutilmoqda,
        'foiz': foiz_hisobla(bajarildi, jami)
    }

# 11. SET
def takrorlanmas_toifalar(toifalar_royxati: list) -> set:
    """Set - to'plam bilan takrorlanishlarni yo'qotish"""
    return set(toifalar_royxati)

# 12. IXCHAM KODLASH (Comprehensions)
def bajarilgan_nomlar(vazifalar) -> list:
    """List comprehension - ixcham ro'yxat tuzish"""
    return [v.sarlavha for v in vazifalar if v.bajarildi]

# 13. REKURSIV FUNKSIYA
def faktorial_yoki_ball(daraja: int) -> int:
    """Rekursiv chaqiruv - o'zini o'zi chaqiruvchi funksiya"""
    if daraja <= 1:
        return 1
    return daraja + faktorial_yoki_ball(daraja - 1)

# 14. ITERATOR
class VazifaIteratori:
    """Maxsus iterator sinfi: __iter__ va __next__"""
    def __init__(self, elementlar):
        self._elementlar = list(elementlar)
        self._indeks = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._indeks < len(self._elementlar):
            qiymat = self._elementlar[self._indeks]
            self._indeks += 1
            return qiymat
        raise StopIteration

# 15. GENERATOR
def vazifa_oqimi(vazifalar):
    """Generator funksiya: yield orqali elementlarni uzatish"""
    for v in vazifalar:
        yield {
            'id': v.id,
            'sarlavha': v.sarlavha,
            'bajarildi': v.bajarildi
        }

# 16. CLOSURES (Ichki funksiyalar)
def vazifa_sanagich(boshlangich: int = 0):
    """Closure - holatni saqlab qoluvchi ichki funksiya"""
    hisob = boshlangich
    def oshir():
        nonlocal hisob
        hisob += 1
        return hisob
    return oshir

# 17. DEKORATORLAR
def vaqt_olchagich(funksiya):
    """Funksiya ishlash vaqtini o'lchovchi oddiy dekorator"""
    @functools.wraps(funksiya)
    def orab_oluvchi(*args, **kwargs):
        boshlanish = time.time()
        natija = funksiya(*args, **kwargs)
        tugash = time.time()
        # Dekorator ishlaganini ko'rsatish
        return natija
    return orab_oluvchi

# 18. OOP (Obyektga yo'naltirilgan dasturlash)
class AsosiyElement:
    """OOP: Baza sinf"""
    def __init__(self, sarlavha: str):
        self.sarlavha = sarlavha

    def malumot(self) -> str:
        return f"Element: {self.sarlavha}"

class ShoshilinchRejaElementi(AsosiyElement):
    """OOP: Merosxo'rlik va polimorfizm"""
    def __init__(self, sarlavha: str, muhimlik: str = 'yuqori'):
        super().__init__(sarlavha)
        self.muhimlik = muhimlik

    def malumot(self) -> str:
        return f"Shoshilinch: {self.sarlavha} [{self.muhimlik}]"

# 19. DATABASE SO'ROVLARI (Raw SQL va ORM so'rovlari)
def togridan_togri_vazifalar_soni(foydalanuvchi_id: int) -> int:
    """To'g'ridan-to'g'ri SQL so'rovi orqali tekshirish"""
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ilova_vazifa WHERE foydalanuvchi_id = %s", [foydalanuvchi_id])
        qator = cursor.fetchone()
        return qator[0] if qator else 0

# 20. PYTHON SQLITE
def sqlite_arxiv_yozish(foydalanuvchi_nomi: str, harakat: str):
    """Python ichki sqlite3 moduli bilan to'g'ridan-to'g'ri ishlash"""
    arxiv_fayli = Path(settings.BASE_DIR) / 'arxiv.sqlite3'
    ulanish = sqlite3.connect(arxiv_fayli)
    kursor = ulanish.cursor()
    kursor.execute('''
        CREATE TABLE IF NOT EXISTS harakatlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            foydalanuvchi TEXT,
            harakat TEXT,
            vaqt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    kursor.execute(
        "INSERT INTO harakatlar (foydalanuvchi, harakat) VALUES (?, ?)",
        (foydalanuvchi_nomi, harakat)
    )
    ulanish.commit()
    ulanish.close()

# 21. ACID TRANSACTIONS
def xavfsiz_vazifa_yaratish(foydalanuvchi, sarlavha, toifa=None, sana=None, vaqt=None, muhimlik='orta'):
    """ACID tranzaksiyasi: transaction.atomic orqali atomik saqlash"""
    from ilova.model import Vazifa
    with transaction.atomic():
        yangi = Vazifa.objects.create(
            foydalanuvchi=foydalanuvchi,
            sarlavha=matnni_tozala(sarlavha),
            toifa=toifa,
            sana=sana,
            vaqt=vaqt,
            muhimlik=muhimlik
        )
        sqlite_arxiv_yozish(foydalanuvchi.username, f"Vazifa yaratildi: {sarlavha}")
        return yangi

# 26. SOFT SKILLS (Maslahatlar va rejalashtirish odatlari)
SOFT_SKILLS_MASLAHATLARI = [
    {
        'sarlavha': "Vaqtni to'g'ri taqsimlash (Time Management)",
        'matn': "Katta vazifalarni 25 daqiqalik qismlarga (Pomodoro) bo'lib bajaring. Bu diqqatni jamlashga yordam beradi."
    },
    {
        'sarlavha': "Ustuvorlikni belgilash (Prioritization)",
        'matn': "Eisenhower matritsasi: muhim va shoshilinch ishlarni birinchi navbatda bajaring, qolganlarini rejalashtiring."
    },
    {
        'sarlavha': "Jamoaviy muloqot madaniyati",
        'matn': "Har bir topshiriqning natijasi va muddatini aniq kelishib oling. Ochiq muloqot xatolarni kamaytiradi."
    },
    {
        'sarlavha': "Doimiy takomillashish (Growth Mindset)",
        'matn': "Kuningiz yakunida 'Bugun nimani yaxshiroq qila olardim?' degan savolga javob bering."
    }
]

def tasodifiy_maslahat():
    """Soft skills maslahatlaridan birini qaytarish"""
    import random
    return random.choice(SOFT_SKILLS_MASLAHATLARI)
