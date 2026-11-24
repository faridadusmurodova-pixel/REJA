# REJA — Shaxsiy Ish Rejalashtirish Tizimi

**REJA** — zamonaviy, to'liq ishlaydigan, ko'p foydalanuvchili (har bir shaxs uchun alohida izolyatsiyalangan) vazifalarni boshqarish dasturi.

---

## 🌟 Asosiy Imkoniyatlar

1. **Ko'p Foydalanuvchili Izolyatsiya:**
   - Sayt ochilganda kirish oynasi chiqadi: **Ism**, **Familiya**, **Yosh** va **Parol**.
   - Har bir foydalanuvchiga unikal identifikator orqali alohida hisob ochiladi.
   - Bir xil ismli shaxslar ham tizimda alohida saqlanadi.
   - Har bir inson faqat o'zining shaxsiy reja va eslatmalarini ko'radi.
2. **Shaxsiy Salomlashuv:** Kirgandan so'ng `"Xush kelibsiz, [Ism]!"` ko'rinishida kutib olinadi.
3. **Rejalar boshqaruvi:** Qo'shish, o'zgartirish, o'chirish, bajarildi deb belgilash, sana va vaqt, muhimlik darajalari (yuqori, o'rta, past), toifalar, qidiruv.
4. **7 ta Asosiy Sahifa:**
   - `Bosh sahifa` (`/`)
   - `Mening rejalarim` (`/rejalar/`)
   - `Bugungi rejalar` (`/bugun/`)
   - `Bajarilganlar` (`/bajarilganlar/`)
   - `Eslatmalar` (`/eslatmalar/`)
   - `Hisobot` (`/hisobot/`)
   - `Profil` (`/profil/`)
   - *Qo'shimcha:* `Foydali blog` (`/blog/`)
5. **Dizayn:** To'q binafsha (`#0b061a`), yashil (`#10b981`), och binafsha (`#8b5cf6`), chiroyli kartochkalar, mobil moslashuvchan.

---

## 📚 41 ta Talab Qilingan Mavzuning Joylashuvi

| № | Mavzu nomi | Qaysi faylda ishlatilgan | Qisqa izoh |
|---|---|---|---|
| 1 | **String** | `ilova/mavzular.py`, `ilova/korinish.py` | `.strip()`, `.capitalize()`, `f-string` matn tozalash |
| 2 | **List** | `ilova/mavzular.py` | `vazifalar_royxatini_tartibla()`, `.sort()`, `.append()` |
| 3 | **Shart operatorlari** | `ilova/mavzular.py`, `ilova/korinish.py` | `if`, `elif`, `else` muhimlik va holat tekshiruvi |
| 4 | **Mantiqiy operatorlar**| `ilova/mavzular.py` | `and`, `or`, `not` mantiqiy tekshiruv |
| 5 | **For sikli** | `ilova/mavzular.py`, `qolip/*.html` | `for v in vazifalar:` sikli orqali aylanish |
| 6 | **While sikli** | `ilova/mavzular.py` | `while son > 0:` orqali qadamli hisoblash |
| 7 | **Funksiya** | `ilova/mavzular.py`, `ilova/korinish.py` | `foiz_hisobla()`, `qosh()`, `saqla()`, `ochir()` |
| 8 | **Copy** | `ilova/mavzular.py`, `ilova/korinish.py` | `copy.copy()` yengil nusxalash |
| 9 | **Deepcopy** | `ilova/mavzular.py`, `ilova/korinish.py` | `copy.deepcopy()` to'liq chuqur nusxa olish |
| 10 | **Dictionary** | `ilova/mavzular.py` | `hisobot_lugati()`, `{ 'jami': x, 'foiz': y }` |
| 11 | **Set** | `ilova/mavzular.py` | `takrorlanmas_toifalar()`, `set()` to'plami |
| 12 | **Ixcham kodlash** | `ilova/mavzular.py`, `ilova/korinish.py` | List comprehension: `[v.sarlavha for v in vazifalar if v.bajarildi]` |
| 13 | **Rekursiv funksiya** | `ilova/mavzular.py` | `faktorial_yoki_ball()` o'zini o'zi chaqiruvchi funksiya |
| 14 | **Iterator** | `ilova/mavzular.py` | `VazifaIteratori` sinfi `__iter__` va `__next__` bilan |
| 15 | **Generator** | `ilova/mavzular.py` | `vazifa_oqimi()` `yield` orqali element uzatish |
| 16 | **Closures** | `ilova/mavzular.py` | `vazifa_sanagich()` ichki yopiq funksiya |
| 17 | **Dekoratorlar** | `ilova/mavzular.py`, `ilova/korinish.py` | `@vaqt_olchagich`, `@login_required` |
| 18 | **OOP** | `ilova/model.py`, `ilova/mavzular.py` | Sinflar, merosxo'rlik, polimorfizm (`AsosiyElement`) |
| 19 | **Database so'rovlari**| `ilova/mavzular.py`, `ilova/korinish.py` | Raw SQL `connection.cursor()` va ORM so'rovlari |
| 20 | **Python SQLite** | `ilova/mavzular.py` | `sqlite3.connect('arxiv.sqlite3')` orqali to'g'ridan-to'g'ri audit |
| 21 | **ACID Transactions** | `ilova/mavzular.py`, `ilova/korinish.py` | `transaction.atomic()` orqali xavfsiz saqlash |
| 22 | **Bot API** | `bot/bot.py` | Telegram Bot API so'rovlari |
| 23 | **Python Telegram Bot**| `bot/bot.py` | `telegram.ext` orqali bot boshqaruvi |
| 24 | **ConversationHandler**| `bot/bot.py` | Muloqotli bosqichma-bosqich reja qo'shish |
| 25 | **PTB botlar** | `bot/bot.py` | ApplicationBuilder orqali to'liq bot |
| 26 | **Soft Skills** | `ilova/mavzular.py`, `qolip/hisob.html` | Vaqtni boshqarish, muloqot, Pomodoro qoidalari |
| 27 | **REST API** | `ilova/serial.py`, `ilova/api.py` | JSON formatidagi CRUD nuqtalari |
| 28 | **Django** | `manage.py`, `reja/soz.py` | Framework arxitekturasi |
| 29 | **URLs va Views** | `reja/yol.py`, `ilova/yol.py` | Marshrutlar va funksional ko'rinishlar |
| 30 | **QuerySetlar** | `ilova/korinish.py` | `.filter()`, `.exclude()`, `.order_by()`, `.count()` |
| 31 | **Django ORM** | `ilova/model.py` | Modellar va munosabatlar |
| 32 | **Django Templates** | `qolip/*.html` | HTML shablonlar |
| 33 | **Jinja formulalari** | `qolip/*.html` | `{% if %}`, `{% for %}`, `{{ user.first_name }}` |
| 34 | **Django ModelForm** | `ilova/forma.py` | `VazifaFormasi`, `EslatmaFormasi`, `ProfilFormasi` |
| 35 | **Blog sayt** | `ilova/korinish.py`, `qolip/blog.html` | Mahsuldorlik bo'yicha maqolalar bo'limi |
| 36 | **Deploy** | `Procfile`, `runtime.txt` | Gunicorn va serverga joylash sozlamalari |
| 37 | **CI/CD** | `.github/workflows/reja.yml` | GitHub Actions avtomatik testlash |
| 38 | **TDD** | `testlar/test_reja.py` | Sinov testlari |
| 39 | **Docker** | `Dockerfile`, `docker-compose.yml` | Konteynerlashtirish |
| 40 | **API** | `ilova/api.py`, `reja/yol.py` | Dasturiy integratsiya interfeysi |
| 41 | **Django REST Framework** | `ilova/serial.py`, `ilova/api.py` | DRF ModelSerializer va ModelViewSet |
| + | **PostgreSQL** | `reja/soz.py`, `docker-compose.yml` | PostgreSQL ulanish sozlamalari |

---

## 🚀 Ishga Tushirish

### 1. Migratsiyalarni bajarish
```bash
python manage.py makemigrations ilova
python manage.py migrate
```

### 2. Boshlang'ich ma'lumotlarni yuklash (Ali, Madina, Jasur va vazifalar)
```bash
python manage.py boshlangich
```

### 3. TDD testlarini ishga tushirish
```bash
python manage.py test testlar
```

### 4. Serverni yoqish
```bash
python manage.py runserver 8000
```
Brauzerda oching: [http://127.0.0.1:8000](http://127.0.0.1:8000)
