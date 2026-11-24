"""
REJA - Ilova URL marshrutlari (yol.py).
Mavzular: URLs va Views, REST API, API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ilova import korinish, api

router = DefaultRouter()
router.register(r'rejalar', api.VazifaViewSet, basename='api_reja')
router.register(r'eslatmalar', api.EslatmaViewSet, basename='api_eslatma')

urlpatterns = [
    # Kirish va hisob
    path('kirish/', korinish.kirish, name='kirish'),
    path('chiqish/', korinish.chiqish, name='chiqish'),
    path('tezkor-kirish/<int:user_id>/', korinish.tezkor_kirish, name='tezkor_kirish'),

    # 7 Asosiy sahifa
    path('', korinish.bosh, name='bosh'),
    path('rejalar/', korinish.rejalar, name='rejalar'),
    path('bugun/', korinish.bugun, name='bugun'),
    path('bajarilganlar/', korinish.bajarilganlar, name='bajarilganlar'),
    path('eslatmalar/', korinish.eslatmalar, name='eslatmalar'),
    path('hisobot/', korinish.hisobot, name='hisobot'),
    path('profil/', korinish.profil, name='profil'),

    # Foydali blog
    path('blog/', korinish.blog, name='blog'),

    # Vazifalar va eslatmalar amallari
    path('qosh/', korinish.qosh, name='qosh'),
    path('saqla/<int:id>/', korinish.saqla, name='saqla'),
    path('ochir/<int:id>/', korinish.ochir, name='ochir'),
    path('bajar/<int:id>/', korinish.bajar, name='bajar'),
    path('nusxa/<int:id>/', korinish.nusxa, name='nusxa'),
    path('eslatma-qosh/', korinish.eslatma_qosh, name='eslatma_qosh'),
    path('eslatma-ochir/<int:id>/', korinish.eslatma_ochir, name='eslatma_ochir'),

    # REST API marshrutlari
    path('api/', include(router.urls)),
    path('api/statistika/', api.StatistikaAPIView.as_view(), name='api_statistika'),
]
