from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from gestion_actu.models import Annonce, Contact, ParametresAgence


User = get_user_model()


class GestionActuApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='agent',
            password='password123',
            first_name='Agent',
            last_name='Test',
            telephone='+22600000000',
        )
        self.annonce = Annonce.objects.create(
            user=self.user,
            type_bien='villa',
            titre='Villa test',
            description='Description test',
            prix=25000000,
            ville='Ouagadougou',
            quartier='Ouaga 2000',
            superficie=300,
        )

    def test_public_can_read_single_agency_settings_object(self):
        ParametresAgence.objects.create(pk=1, nom_agence='MyCitiNest Test')

        response = self.client.get('/api/gestion_actu/parametres/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['nom_agence'], 'MyCitiNest Test')

    def test_public_contact_creation_forces_unread_status(self):
        response = self.client.post(
            '/api/gestion_actu/contacts/',
            {
                'annonce': self.annonce.pk,
                'nom': 'Client Test',
                'telephone': '+22611111111',
                'email': 'client@example.com',
                'message': 'Je suis interesse.',
                'lu': True,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contact = Contact.objects.get()
        self.assertFalse(contact.lu)

    def test_authenticated_user_can_create_annonce_with_ordered_media(self):
        self.client.force_authenticate(self.user)
        payload = {
            'type_bien': 'terrain',
            'titre': 'Terrain avec medias',
            'description': 'Une annonce avec photos et videos.',
            'prix': 12000000,
            'ville': 'Bobo-Dioulasso',
            'quartier': 'Belle Ville',
            'telephone': '+22670000000',
            'superficie': 500,
            'photos': [
                SimpleUploadedFile('first.jpg', b'first-image', content_type='image/jpeg'),
                SimpleUploadedFile('second.jpg', b'second-image', content_type='image/jpeg'),
            ],
            'videos': [
                SimpleUploadedFile('first.mp4', b'first-video', content_type='video/mp4'),
                SimpleUploadedFile('second.mp4', b'second-video', content_type='video/mp4'),
            ],
        }

        response = self.client.post('/api/gestion_actu/annonces/', payload, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        annonce = Annonce.objects.get(titre='Terrain avec medias')
        self.assertEqual(list(annonce.photos.values_list('ordre', flat=True)), [0, 1])
        self.assertEqual(list(annonce.videos.values_list('ordre', flat=True)), [0, 1])
        self.assertEqual(annonce.user, self.user)
        self.assertEqual(annonce.telephone, '+22670000000')
