from django.urls import path, include
from rest_framework.routers import DefaultRouter
# pyrefly: ignore [missing-import]
from .views import (
    RegisterView, LogoutView, AnnonceViewSet, MyTokenObtainPairView
)

router = DefaultRouter()
router.register(r'annonces', AnnonceViewSet, basename='annonce')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', MyTokenObtainPairView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
