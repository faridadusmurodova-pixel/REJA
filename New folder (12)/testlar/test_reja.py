"""
REJA - Test-Driven Development (TDD) test to'plami (testlar/test_reja.py).
Mavzular: TDD, Django ORM, QuerySetlar, REST API, ACID Transactions.
"""
from django.test import TestCase, Client
from django.urls import reverse
from ilova.model import Foydalanuvchi, Vazifa, Toifa
from ilova import mavzular

class ShaxsiyRejaTestlari(TestCase):
    """Foydalanuvchilar izolyatsiyasi va asosiy imkoniyatlar testi"""

    def setUp(self):
        # 1. Ikkita turli foydalanuvchi yaratish
        self.ali = Foydalanuvchi.objects.create_user(
            username='ali_valiyev_25',
            first_name='Ali',
            last_name='Valiyev',
            yosh=25,
            password='parol_ali_123'
        )
        self.madina = Foydalanuvchi.objects.create_user(
            username='madina_karimova_23',
            first_name='Madina',
            last_name='Karimova',
            yosh=23,
            password='parol_madina_123'
        )

        # 2. Har biriga alohida vazifalar biriktirish
        self.vazifa_ali = Vazifa.objects.create(
            foydalanuvchi=self.ali,
            sarlavha="Ali ning shaxsiy dasturlash rejasi",
            muhimlik='yuqori'
        )
        self.vazifa_madina = Vazifa.objects.create(
            foydalanuvchi=self.madina,
            sarlavha="Madina ning dizayn loyihasi",
            muhimlik='yuqori'
        )

    def test_foydalanuvchi_izolyatsiyasi(self):
        """
        ENG MUHIM TALAB: Ali Madinaning rejalarini ko'ra olmasligi kerak.
        """
        ali_rejalari = Vazifa.objects.filter(foydalanuvchi=self.ali)
        madina_rejalari = Vazifa.objects.filter(foydalanuvchi=self.madina)

        self.assertEqual(ali_rejalari.count(), 1)
        self.assertEqual(madina_rejalari.count(), 1)
        self.assertIn(self.vazifa_ali, ali_rejalari)
        self.assertNotIn(self.vazifa_madina, ali_rejalari)

    def test_foydalanuvchi_xususiyatlari(self):
        """Foydalanuvchi modeli yosh, ism va metodlari to'g'ri ishlashi"""
        self.assertEqual(self.ali.ism, 'Ali')
        self.assertEqual(self.ali.yosh, 25)
        self.assertEqual(self.ali.jami_vazifalar(), 1)
        self.assertEqual(self.ali.bajarilgan_vazifalar(), 0)
        self.assertEqual(self.ali.bajarilish_foizi(), 0)

        # Vazifani bajarilgan deb belgilash
        self.vazifa_ali.bajarildi = True
        self.vazifa_ali.save()
        self.assertEqual(self.ali.bajarilgan_vazifalar(), 1)
        self.assertEqual(self.ali.bajarilish_foizi(), 100)

    def test_41_mavzular_funksiyalari(self):
        """Python va baza mavzularining sodda funksiyalarini sinash"""
        # String
        self.assertEqual(mavzular.matnni_tozala("  salom dunyo  "), "Salom dunyo")
        # List
        saralangan = mavzular.vazifalar_royxatini_tartibla([self.vazifa_ali])
        self.assertEqual(len(saralangan), 1)
        # Shart operatori
        self.assertEqual(mavzular.muhimlik_rangi('yuqori'), '#ef4444')
        # Mantiqiy operator
        self.assertTrue(mavzular.shoshilinchmi('yuqori', False))
        # Copy va Deepcopy
        lugat = {'ism': 'Ali', 'reja': {'nomi': 'Backend'}}
        nusxa_chuqur = mavzular.toliq_reja_nusxasi(lugat)
        self.assertEqual(nusxa_chuqur['reja']['nomi'], 'Backend')
        # Set
        toifalar = mavzular.takrorlanmas_toifalar(['Ish', 'Ish', 'O\'qish'])
        self.assertEqual(len(toifalar), 2)
        # Ixcham kodlash (List comprehension)
        bajarilganlar = mavzular.bajarilgan_nomlar([self.vazifa_ali])
        self.assertEqual(len(bajarilganlar), 0)
        # Closure
        sanagich = mavzular.vazifa_sanagich(5)
        self.assertEqual(sanagich(), 6)
        # Iterator
        it = mavzular.VazifaIteratori(['A', 'B'])
        self.assertEqual(next(it), 'A')
        self.assertEqual(next(it), 'B')

    def test_veb_sahifalar_ishlashi(self):
        """Web sahifalarga kirish va 200 OK qaytishi"""
        klient = Client()
        klient.force_login(self.ali)

        sahifalar = ['bosh', 'rejalar', 'bugun', 'bajarilganlar', 'eslatmalar', 'hisobot', 'profil', 'blog']
        for s in sahifalar:
            javob = klient.get(reverse(s))
            self.assertEqual(javob.status_code, 200, f"{s} sahifasi xato berdi!")
