from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from simplemooc.courses.models import Course

class ContactCourseTestCase(TestCase):

    # Método inicial executado antes de iniciar os testes da classe
    @classmethod
    def setUpClass(cls):
        pass

    # Método final executado após o término dos testes da classe
    @classmethod
    def tearDownClass(cls):
        pass

    # Método inicial executado antes de cada método da classe de testes
    def setUp(self):
        self.course = Course.objects.create(name="Django", slug="django")

    # Método final executado após cada método da classe de testes
    def tearDown(self):
        self.course.delete()

    # Método para verificar erro na inclusão de um curso
    def test_contact_form_error(self):
        data = {'name': 'Fulano de tal', 'email':'', 'message':''}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    # Método para verificar o envio de email ao enviar uma dúvida do curso
    def test_contact_form_success_send_mail(self):
        data = {'name': 'Fulano de tal', 'email':'fulanodetal@gmail.com', 'message':'Bem vindo'}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertEqual(len(mail.outbox), 1)
        #self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])
