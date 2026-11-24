"""
REJA - REST API ViewSet va API nuqtalari (api.py).
Mavzular: REST API, Django REST Framework, API.
"""
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from ilova.model import Vazifa, Eslatma, Toifa
from ilova.serial import VazifaSerializer, EslatmaSerializer, ToifaSerializer

class VazifaViewSet(viewsets.ModelViewSet):
    """
    Shaxsiy vazifalar uchun REST API CRUD amallari.
    Faqat tizimga kirgan foydalanuvchining o'z ma'lumotlarini qaytaradi.
    """
    serializer_class = VazifaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vazifa.objects.filter(foydalanuvchi=self.request.user)

    def perform_create(self, serializer):
        serializer.save(foydalanuvchi=self.request.user)


class EslatmaViewSet(viewsets.ModelViewSet):
    """Eslatmalar uchun REST API"""
    serializer_class = EslatmaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Eslatma.objects.filter(foydalanuvchi=self.request.user)

    def perform_create(self, serializer):
        serializer.save(foydalanuvchi=self.request.user)


class StatistikaAPIView(APIView):
    """Foydalanuvchi statistikasi API nuqtasi"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        f = request.user
        return Response({
            'foydalanuvchi': f.toliq_ism,
            'yosh': f.yosh,
            'jami': f.jami_vazifalar(),
            'bajarilgan': f.bajarilgan_vazifalar(),
            'bajarilmagan': f.bajarilmagan_vazifalar(),
            'bugun': f.bugungi_vazifalar(),
            'foiz': f.bajarilish_foizi(),
        })
