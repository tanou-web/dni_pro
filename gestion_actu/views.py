from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from gestion_actu.models import Annonce, Photo, Video, Contact, ParametresAgence, HomeFeature, Partner
from gestion_actu.serializers import (
    RegisterSerializer, AnnonceSerializer, UserSerializer,
    MyTokenObtainPairSerializer, ContactSerializer,
    ParametresAgenceSerializer, UserAdminSerializer,
    CurrentUserSerializer, PasswordChangeSerializer,
    HomeFeatureSerializer, PartnerSerializer,
)

User = get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
   
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Utilisateur créé avec succès.",
        }, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Le token de rafraîchissement est requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"error": "Token invalide ou déjà révoqué."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserAdminSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ('me', 'change_password'):
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'me':
            return CurrentUserSerializer
        if self.action == 'change_password':
            return PasswordChangeSerializer
        return UserAdminSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.pk == request.user.pk:
            return Response(
                {"error": "Vous ne pouvez pas supprimer votre propre compte."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='me/password')
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Mot de passe modifie avec succes."})


# --- Annonce ViewSet ---
class AnnonceViewSet(viewsets.ModelViewSet):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user if (self.request.user and self.request.user.is_authenticated) else None
        if not user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Authentication credentials were not provided.')
        annonce = serializer.save(user=user)
        
        # Save uploaded photos
        photos = self.request.FILES.getlist('photos')
        for index, photo_file in enumerate(photos):
            Photo.objects.create(annonce=annonce, image=photo_file, ordre=index)
            
        # Save uploaded videos
        videos = self.request.FILES.getlist('videos')
        for index, video_file in enumerate(videos):
            Video.objects.create(annonce=annonce, video=video_file, ordre=index)

    def perform_update(self, serializer):
        annonce = serializer.save()
        clear_photos = self.request.data.get('clear_photos') in ('true', '1', True)
        clear_videos = self.request.data.get('clear_videos') in ('true', '1', True)
        
        # Replace photos if new ones are uploaded
        if clear_photos or 'photos' in self.request.FILES:
            annonce.photos.all().delete()
            photos = self.request.FILES.getlist('photos')
            for index, photo_file in enumerate(photos):
                Photo.objects.create(annonce=annonce, image=photo_file, ordre=index)
                
        # Replace videos if new ones are uploaded
        if clear_videos or 'videos' in self.request.FILES:
            annonce.videos.all().delete()
            videos = self.request.FILES.getlist('videos')
            for index, video_file in enumerate(videos):
                Video.objects.create(annonce=annonce, video=video_file, ordre=index)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.select_related('annonce').all()
    serializer_class = ContactSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(lu=False)


class ParametresAgenceViewSet(viewsets.ModelViewSet):
    serializer_class = ParametresAgenceSerializer

    def get_queryset(self):
        return ParametresAgence.objects.all()

    def get_object(self):
        obj, _ = ParametresAgence.objects.get_or_create(pk=1)
        return obj

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)


class HomeFeatureViewSet(viewsets.ModelViewSet):
    queryset = HomeFeature.objects.all()
    serializer_class = HomeFeatureSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = HomeFeature.objects.all()
        if self.action in ('list', 'retrieve') and not self.request.user.is_authenticated:
            queryset = queryset.filter(actif=True)
        return queryset


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = Partner.objects.all()
        if self.action in ('list', 'retrieve') and not self.request.user.is_authenticated:
            queryset = queryset.filter(actif=True)
        return queryset
