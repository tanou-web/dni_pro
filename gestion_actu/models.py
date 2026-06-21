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
        ordering = ['-pk']
        db_table = 'photo'
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
        


class Contact(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Favori(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'annonce')