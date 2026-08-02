from django.urls import path, include
from rest_framework.routers import DefaultRouter
# pyrefly: ignore [missing-import]
from .views import (
    RegisterView, LogoutView, AnnonceViewSet, MyTokenObtainPairView,
    ContactViewSet, ParametresAgenceViewSet,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'annonces', AnnonceViewSet, basename='annonce')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'parametres', ParametresAgenceViewSet, basename='parametres')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', MyTokenObtainPairView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
