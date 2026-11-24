"""
REJA - Asosiy ko'rinishlar va mantiq (korinish.py).
Mavzular: Django, URLs va Views, QuerySetlar, Django Templates, ACID Transactions,
String, List, Shart operatorlari, Mantiqiy operatorlar, For, While, Funksiya,
Copy, Deepcopy, Dictionary, Set, Ixcham kodlash, Iterator, Generator, Closures, Dekoratorlar.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import date

from ilova.model import Foydalanuvchi, Vazifa, Toifa, Eslatma, Maqola
from ilova.forma import VazifaFormasi, EslatmaFormasi, ProfilFormasi
from ilova import mavzular

# KIRISH VA RO'YXATDAN O'TISH
def kirish(request):
    """
    1. Kirish oynasi:
    Foydalanuvchidan Ism, Familiya, Yosh va Parol so'raladi.
    Kiritilgan ism-familiyaga mos yangi shaxsiy hisob yaratiladi yoki mavjud hisobiga kiriladi.
    Barcha rejalar o'sha odam uchun xavfsiz saqlanib qoladi.
    """
    if request.user.is_authenticated:
        return redirect('bosh')

    if request.method == 'POST':
        ism = mavzular.matnni_tozala(request.POST.get('ism', ''))
        familiya = mavzular.matnni_tozala(request.POST.get('familiya', ''))
        yosh_str = request.POST.get('yosh', '20')
        parol = request.POST.get('parol', '').strip()

        try:
            yosh = int(yosh_str)
        except ValueError:
            yosh = 20

        if not ism or not parol:
            messages.error(request, "Iltimos, ism va parolni to'liq kiriting!")
            return redirect('kirish')

        # Avval shunday ism va familiyali foydalanuvchi bormi tekshirish
        user = Foydalanuvchi.objects.filter(first_name__iexact=ism, last_name__iexact=familiya).first()

        if not user:
            # Username bo'yicha ham tekshirib ko'ramiz
            taxminiy_login = f"{ism.lower()}_{familiya.lower() if familiya else 'shaxs'}_{yosh}"
            user = Foydalanuvchi.objects.filter(username=taxminiy_login).first()

        if user:
            # Agar mavjud bo'lsa parolini tekshiramiz
            if user.check_password(parol):
                login(request, user)
                mavzular.sqlite_arxiv_yozish(user.username, "Tizimga kirdi")
                messages.success(request, f"Xush kelibsiz, {user.first_name}!")
                return redirect('bosh')
            else:
                messages.error(request, "Bu ismdagi hisob uchun kiritilgan parol noto'g'ri!")
                return redirect('kirish')
        else:
            # Yangi unikal shaxsiy foydalanuvchi hisobini yaratamiz
            asosiy_login = f"{ism.lower()}_{familiya.lower() if familiya else 'shaxs'}_{yosh}"
            takroriy_soni = Foydalanuvchi.objects.filter(username__startswith=asosiy_login).count()
            if takroriy_soni > 0:
                asosiy_login = f"{asosiy_login}_{takroriy_soni + 1}"

            yangi_user = Foydalanuvchi.objects.create_user(
                username=asosiy_login,
                first_name=ism,
                last_name=familiya,
                yosh=yosh,
                password=parol
            )
            login(request, yangi_user)
            mavzular.sqlite_arxiv_yozish(yangi_user.username, "Yangi shaxsiy hisob ochildi va kirdi")
            messages.success(request, f"Xush kelibsiz, {ism}! Sizning shaxsiy ish reja hisobingiz yaratildi.")
            return redirect('bosh')

    mavjud_foydalanuvchilar = Foydalanuvchi.objects.filter(is_superuser=False).order_by('-date_joined')
    return render(request, 'kirish.html', {'mavjud_foydalanuvchilar': mavjud_foydalanuvchilar})


def tezkor_kirish(request, user_id):
    """Mavjud foydalanuvchi hisobiga tezkor o'tish"""
    user = get_object_or_404(Foydalanuvchi, id=user_id)
    login(request, user)
    messages.success(request, f"Xush kelibsiz, {user.first_name}!")
    return redirect('bosh')


def chiqish(request):
    """Tizimdan chiqish"""
    logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('kirish')


# 1. BOSH SAHIFA
@login_required
@mavzular.vaqt_olchagich
def bosh(request):
    """
    Bosh sahifa:
    - Xush kelibsiz, [Ism]!
    - Shaxsiy rejalar xulosasi
    - Bugungi rejalar
    - Yangi reja qo'shish
    """
    user = request.user
    bugun = timezone.now().date()
    
    # Faqat ushbu foydalanuvchining shaxsiy vazifalari (Izolyatsiya)
    foydalanuvchi_vazifalari = Vazifa.objects.filter(foydalanuvchi=user)
    bugungi_rejalar = foydalanuvchi_vazifalari.filter(sana=bugun)
    songi_rejalar = foydalanuvchi_vazifalari[:6]

    jami = foydalanuvchi_vazifalari.count()
    bajarildi = foydalanuvchi_vazifalari.filter(bajarildi=True).count()
    kutilmoqda = jami - bajarildi
    hisobot = mavzular.hisobot_lugati(jami, bajarildi, kutilmoqda)

    toifalar = Toifa.objects.filter(Q(foydalanuvchi=user) | Q(foydalanuvchi__isnull=True))

    kontekst = {
        'sahifa': 'bosh',
        'hisobot': hisobot,
        'bugungi_rejalar': bugungi_rejalar,
        'songi_rejalar': songi_rejalar,
        'toifalar': toifalar,
        'maslahat': mavzular.tasodifiy_maslahat(),
        'hozirgi_sana': bugun,
    }
    return render(request, 'bosh.html', kontekst)


# 2. MENING REJALARIM
@login_required
def rejalar(request):
    """Mening rejalarim: barcha shaxsiy rejalar, qidiruv va filtrlash"""
    user = request.user
    vazifalar = Vazifa.objects.filter(foydalanuvchi=user)

    qidiruv = request.GET.get('qidiruv', '').strip()
    if qidiruv:
        vazifalar = vazifalar.filter(
            Q(sarlavha__icontains=qidiruv) | Q(tavsif__icontains=qidiruv)
        )

    toifa_id = request.GET.get('toifa')
    if toifa_id:
        vazifalar = vazifalar.filter(toifa_id=toifa_id)

    holat = request.GET.get('holat')
    if holat == 'bajarildi':
        vazifalar = vazifalar.filter(bajarildi=True)
    elif holat == 'kutilmoqda':
        vazifalar = vazifalar.filter(bajarildi=False)

    toifalar = Toifa.objects.filter(Q(foydalanuvchi=user) | Q(foydalanuvchi__isnull=True))

    kontekst = {
        'sahifa': 'rejalar',
        'vazifalar': vazifalar,
        'toifalar': toifalar,
        'tanlangan_toifa': toifa_id,
        'tanlangan_holat': holat,
        'qidiruv': qidiruv,
    }
    return render(request, 'rejalar.html', kontekst)


# 3. BUGUNGI REJALAR
@login_required
def bugun(request):
    """Bugungi rejalar"""
    user = request.user
    bugungi_sana = timezone.now().date()
    vazifalar = Vazifa.objects.filter(foydalanuvchi=user, sana=bugungi_sana)

    kontekst = {
        'sahifa': 'bugun',
        'vazifalar': vazifalar,
        'bugungi_sana': bugungi_sana,
    }
    return render(request, 'bugun.html', kontekst)


# 4. BAJARILGANLAR
@login_required
def bajarilganlar(request):
    """Bajarilgan rejalar arxivi"""
    user = request.user
    vazifalar = Vazifa.objects.filter(foydalanuvchi=user, bajarildi=True)
    nomlar = mavzular.bajarilgan_nomlar(vazifalar)

    kontekst = {
        'sahifa': 'bajarilganlar',
        'vazifalar': vazifalar,
        'bajarilgan_nomlar': nomlar,
    }
    return render(request, 'bajarilganlar.html', kontekst)


# 5. ESLATMALAR
@login_required
def eslatmalar(request):
    """Shaxsiy eslatmalar"""
    user = request.user
    eslatma_royxati = Eslatma.objects.filter(foydalanuvchi=user)

    forma = EslatmaFormasi()
    kontekst = {
        'sahifa': 'eslatmalar',
        'eslatmalar': eslatma_royxati,
        'forma': forma,
    }
    return render(request, 'eslatma.html', kontekst)


# 6. HISOBOT
@login_required
def hisobot(request):
    """Shaxsiy hisobot va foizlar"""
    user = request.user
    vazifalar = Vazifa.objects.filter(foydalanuvchi=user)
    
    jami = vazifalar.count()
    bajarilgan = vazifalar.filter(bajarildi=True).count()
    bajarilmagan = jami - bajarilgan
    bugun_soni = vazifalar.filter(sana=timezone.now().date()).count()
    foiz = mavzular.foiz_hisobla(bajarilgan, jami)

    yuqori_soni = vazifalar.filter(muhimlik='yuqori').count()
    orta_soni = vazifalar.filter(muhimlik='orta').count()
    past_soni = vazifalar.filter(muhimlik='past').count()

    toifalar_set = mavzular.takrorlanmas_toifalar([v.toifa.nomi for v in vazifalar if v.toifa])

    kontekst = {
        'sahifa': 'hisobot',
        'jami': jami,
        'bajarilgan': bajarilgan,
        'bajarilmagan': bajarilmagan,
        'bugun_soni': bugun_soni,
        'foiz': foiz,
        'yuqori_soni': yuqori_soni,
        'orta_soni': orta_soni,
        'past_soni': past_soni,
        'toifalar_soni': len(toifalar_set),
        'maslahatlar': mavzular.SOFT_SKILLS_MASLAHATLARI,
    }
    return render(request, 'hisob.html', kontekst)


# 7. PROFIL
@login_required
def profil(request):
    """Foydalanuvchi shaxsiy profili"""
    user = request.user
    if request.method == 'POST':
        forma = ProfilFormasi(request.POST, instance=user)
        if forma.is_valid():
            forma.save()
            messages.success(request, "Profilingiz muvaffaqiyatli yangilandi!")
            return redirect('profil')
    else:
        forma = ProfilFormasi(instance=user)

    boshqa_foydalanuvchilar = Foydalanuvchi.objects.exclude(id=user.id)

    kontekst = {
        'sahifa': 'profil',
        'forma': forma,
        'user': user,
        'boshqa_foydalanuvchilar': boshqa_foydalanuvchilar,
    }
    return render(request, 'profil.html', kontekst)


# BLOG SAHIFA
@login_required
def blog(request):
    """Foydali maqolalar"""
    maqolalar = Maqola.objects.all().order_by('-sana')
    return render(request, 'blog.html', {'sahifa': 'blog', 'maqolalar': maqolalar})


# AMALLAR
@login_required
def qosh(request):
    """Yangi reja / vazifa qo'shish"""
    user = request.user
    if request.method == 'POST':
        sarlavha = request.POST.get('sarlavha', '').strip()
        tavsif = request.POST.get('tavsif', '').strip()
        sana = request.POST.get('sana') or timezone.now().date()
        vaqt = request.POST.get('vaqt') or None
        muhimlik = request.POST.get('muhimlik', 'orta')
        toifa_id = request.POST.get('toifa')

        toifa = Toifa.objects.filter(id=toifa_id).first() if toifa_id else None

        if sarlavha:
            mavzular.xavfsiz_vazifa_yaratish(
                foydalanuvchi=user,
                sarlavha=sarlavha,
                toifa=toifa,
                sana=sana,
                vaqt=vaqt,
                muhimlik=muhimlik
            )
            messages.success(request, "Yangi reja qo'shildi va saqlandi!")
        else:
            messages.error(request, "Reja sarlavhasini kiritishingiz shart!")

    qayerdan = request.META.get('HTTP_REFERER')
    return redirect(qayerdan if qayerdan else 'bosh')


@login_required
def saqla(request, id):
    """Rejani tahrirlash"""
    vazifa = get_object_or_404(Vazifa, id=id, foydalanuvchi=request.user)

    if request.method == 'POST':
        forma = VazifaFormasi(request.POST, instance=vazifa, foydalanuvchi=request.user)
        if forma.is_valid():
            forma.save()
            messages.success(request, "Reja yangilandi!")
            return redirect('rejalar')
    else:
        forma = VazifaFormasi(instance=vazifa, foydalanuvchi=request.user)

    return render(request, 'saqla.html', {'forma': forma, 'vazifa': vazifa, 'sahifa': 'rejalar'})


@login_required
def ochir(request, id):
    """Rejani o'chirish"""
    vazifa = get_object_or_404(Vazifa, id=id, foydalanuvchi=request.user)
    nomi = vazifa.sarlavha
    vazifa.delete()
    mavzular.sqlite_arxiv_yozish(request.user.username, f"Vazifa o'chirildi: {nomi}")
    messages.info(request, f"'{nomi}' rejasi o'chirildi.")
    qayerdan = request.META.get('HTTP_REFERER')
    return redirect(qayerdan if qayerdan else 'rejalar')


@login_required
def bajar(request, id):
    """Vazifani bajarildi / kutilmoqda holatiga o'tkazish"""
    vazifa = get_object_or_404(Vazifa, id=id, foydalanuvchi=request.user)
    vazifa.bajarildi = not vazifa.bajarildi
    vazifa.save()
    holat_matni = "bajarildi" if vazifa.bajarildi else "kutilmoqda holatiga qaytarildi"
    mavzular.sqlite_arxiv_yozish(request.user.username, f"Vazifa holati: {vazifa.sarlavha} -> {holat_matni}")
    messages.success(request, f"'{vazifa.sarlavha}' {holat_matni}!")
    qayerdan = request.META.get('HTTP_REFERER')
    return redirect(qayerdan if qayerdan else 'bosh')


@login_required
def nusxa(request, id):
    """Rejadan nusxa olish (Copy/Deepcopy)"""
    vazifa = get_object_or_404(Vazifa, id=id, foydalanuvchi=request.user)
    malumot = {
        'sarlavha': f"{vazifa.sarlavha} (Nusxa)",
        'tavsif': vazifa.tavsif,
        'toifa': vazifa.toifa,
        'sana': vazifa.sana,
        'vaqt': vazifa.vaqt,
        'muhimlik': vazifa.muhimlik
    }
    yangi_malumot = mavzular.toliq_reja_nusxasi(malumot)
    Vazifa.objects.create(foydalanuvchi=request.user, **yangi_malumot)
    messages.success(request, f"'{vazifa.sarlavha}' nusxalandi!")
    return redirect('rejalar')


@login_required
def eslatma_qosh(request):
    """Yangi eslatma yozish"""
    if request.method == 'POST':
        sarlavha = request.POST.get('sarlavha', '').strip()
        matn = request.POST.get('matn', '').strip()
        rang = request.POST.get('rang', '#ffffff')
        muhim = request.POST.get('muhim') == 'on'
        if sarlavha and matn:
            Eslatma.objects.create(
                foydalanuvchi=request.user,
                sarlavha=sarlavha,
                matn=matn,
                rang=rang,
                muhim=muhim
            )
            messages.success(request, "Eslatma saqlandi!")
    return redirect('eslatmalar')


@login_required
def eslatma_ochir(request, id):
    """Eslatmani o'chirish"""
    eslatma = get_object_or_404(Eslatma, id=id, foydalanuvchi=request.user)
    eslatma.delete()
    messages.info(request, "Eslatma o'chirildi.")
    return redirect('eslatmalar')
