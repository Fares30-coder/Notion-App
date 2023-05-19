from django.test import TestCase, Client
from django.urls import reverse

class MyAPITestCase(TestCase):
    def setUp(self):
        # Code exécuté avant chaque test
        self.client = Client()

    def test_my_endpoint(self):
        # Code de test pour votre point d'extrémité
        url = reverse('')   
        response = self.client.get(url)
        
        # Assertions pour vérifier la réponse
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Success'})

# Create your tests here.
