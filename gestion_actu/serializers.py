from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from gestion_actu.models import Annonce, Photo, Video, Contact, Favori, ParametresAgence

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'telephone')
        read_only_fields = ('id',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'telephone')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', ''),
            telephone=validated_data.get('telephone', '')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class PhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('id', 'annonce', 'image', 'image_url', 'ordre')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        if obj.image:
            return obj.image.url
        return ''

class VideoSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('id', 'annonce', 'video', 'video_url', 'ordre')

    def get_video_url(self, obj):
        request = self.context.get('request')
        if obj.video and request:
            return request.build_absolute_uri(obj.video.url)
        if obj.video:
            return obj.video.url
        return ''

class AnnonceSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Annonce
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favori
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    bien_concerne = serializers.CharField(source='annonce.titre', read_only=True)

    class Meta:
        model = Contact
        fields = ('id', 'annonce', 'bien_concerne', 'nom', 'telephone', 'email', 'message', 'lu', 'created_at')

class ParametresAgenceSerializer(serializers.ModelSerializer):
    logo_image_url = serializers.SerializerMethodField()
    hero_image_url = serializers.SerializerMethodField()

    class Meta:
        model = ParametresAgence
        fields = (
            'id', 'nom_agence', 'telephone', 'whatsapp', 'email', 'adresse',
            'site_web', 'facebook', 'instagram', 'logo_image', 'logo_image_url',
            'hero_image', 'hero_image_url', 'updated_at',
        )
        read_only_fields = ('id', 'updated_at')

    def get_logo_image_url(self, obj):
        request = self.context.get('request')
        if obj.logo_image and request:
            return request.build_absolute_uri(obj.logo_image.url)
        if obj.logo_image:
            return obj.logo_image.url
        return ''

    def get_hero_image_url(self, obj):
        request = self.context.get('request')
        if obj.hero_image and request:
            return request.build_absolute_uri(obj.hero_image.url)
        if obj.hero_image:
            return obj.hero_image.url
        return ''
