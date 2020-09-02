from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

class HomeViewTest(TestCase):

    # Teste para verificar a disponibilidade da páginaa inicial da aplicação
    def test_home_status_code(self):
        client = Client()
        response = client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    # Teste para verificar se o template ESTÁ sendo usado na página inicial
    def test_home_template_used(self):
        client = Client()
        response = client.get(reverse('core:home'))
        self.assertTemplateUsed(response, "home.html")

    # Teste para verificar se o template NÃO está sendo usado na página inicial
    def test_home_template_not_used(self):
        client = Client()
        response = client.get(reverse('core:home'))
        self.assertTemplateNotUsed(response, "not_used.html")
