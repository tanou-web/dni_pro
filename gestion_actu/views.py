from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from gestion_actu.models import Annonce, Photo, Video, Contact, ParametresAgence
from gestion_actu.serializers import (
    RegisterSerializer, AnnonceSerializer, UserSerializer,
    MyTokenObtainPairSerializer, ContactSerializer,
    ParametresAgenceSerializer,
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
        
        # Replace photos if new ones are uploaded
        if 'photos' in self.request.FILES:
            annonce.photos.all().delete()
            photos = self.request.FILES.getlist('photos')
            for index, photo_file in enumerate(photos):
                Photo.objects.create(annonce=annonce, image=photo_file, ordre=index)
                
        # Replace videos if new ones are uploaded
        if 'videos' in self.request.FILES:
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
