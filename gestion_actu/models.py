from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telephone']

class Annonce(models.Model):
    TYPE_BIEN = [
        ('terrain', 'Terrain'),
        ('villa', 'Villa'),
        ('parcelle', 'Parcelle'),
        ('champ', 'Champ'),
    ]
    STATUT = [
        ('disponible', 'Disponible'),
        ('vendu', 'Vendu'),
        ('archive', 'Archivé'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type_bien = models.CharField(max_length=20, choices=TYPE_BIEN)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=12, decimal_places=0)
    ville = models.CharField(max_length=100)
    quartier = models.CharField(max_length=100)
    telephone = models.CharField(max_length=30, blank=True)
    superficie = models.FloatField()
    statut = models.CharField(max_length=20, choices=STATUT, default='disponible')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']
        db_table = 'annonce'
        verbose_name = 'Annonce'
        verbose_name_plural = 'Annonces'
       


    def full_info(self):
        return f'{self.type_bien}- {self.prix}-{self.statut}'

    def __str__(self):
        return f"{self.full_info}-{self.titre} - {self.ville}"


    

class Photo(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='annonces/')
    ordre = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordre', 'pk']
        db_table = 'photo'
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def __str__(self):
        return f"{self.annonce.titre} - photo {self.ordre + 1}"


class Video(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='annonces/videos/')
    ordre = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordre', 'pk']
        db_table = 'video'
        verbose_name = 'Vidéo'
        verbose_name_plural = 'Vidéos'

    def __str__(self):
        return f"{self.annonce.titre} - vidéo {self.ordre + 1}"


class Contact(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='contacts')
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField()
    lu = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'contact'
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'

    def __str__(self):
        return f"{self.nom} - {self.annonce.titre}"


class Favori(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoris')
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='favoris')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'favori'
        verbose_name = 'Favori'
        verbose_name_plural = 'Favoris'
        unique_together = ('user', 'annonce')

    def __str__(self):
        return f"{self.user.username} → {self.annonce.titre}"


class ParametresAgence(models.Model):
    nom_agence = models.CharField(max_length=120, default='MyCitiNest')
    telephone = models.CharField(max_length=30, default='+226 65 17 04 60')
    whatsapp = models.CharField(max_length=30, default='+226 65 17 04 60')
    email = models.EmailField(default='contact@mycitinest.com')
    adresse = models.CharField(max_length=255, default='Ouaga 2000, Ouagadougou, Burkina Faso')
    site_web = models.URLField(blank=True, default='https://www.mycitinest.com')
    facebook = models.URLField(blank=True, default='https://facebook.com/mycitinest')
    instagram = models.URLField(blank=True, default='https://instagram.com/mycitinest')
    logo_image = models.ImageField(upload_to='agence/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='agence/', blank=True, null=True)
    
    feature1_title = models.CharField(max_length=100, default='Site officiel')
    feature1_desc = models.CharField(max_length=200, default='Zéro arnaque')
    
    feature2_title = models.CharField(max_length=100, default='Annonces vérifiées')
    feature2_desc = models.CharField(max_length=200, default='Biens contrôlés')
    
    feature3_title = models.CharField(max_length=100, default='Accompagnement')
    feature3_desc = models.CharField(max_length=200, default='Conseils personnalisés')
    
    feature4_title = models.CharField(max_length=100, default='Transactions sécurisées')
    feature4_desc = models.CharField(max_length=200, default='En toute simplicité')
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parametres_agence'
        verbose_name = 'Parametres agence'
        verbose_name_plural = 'Parametres agence'

    def __str__(self):
        return self.nom_agence


class HomeFeature(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    ordre = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordre', 'pk']
        db_table = 'home_feature'
        verbose_name = 'Champ accueil'
        verbose_name_plural = 'Champs accueil'

    def __str__(self):
        return self.title


class Partner(models.Model):
    nom = models.CharField(max_length=120)
    description = models.CharField(max_length=220, blank=True)
    site_web = models.URLField(blank=True)
    logo = models.ImageField(upload_to='partenaires/', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordre', 'pk']
        db_table = 'partner'
        verbose_name = 'Partenaire'
        verbose_name_plural = 'Partenaires'

    def __str__(self):
        return self.nom
