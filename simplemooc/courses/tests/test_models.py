from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

# Biblioteca para preenchimento automático de models
from model_mommy import mommy

from simplemooc.courses.models import Course

class CourseManagerTestCase(TestCase):

    # Método inicial executado antes de cada método da classe de testes
    def setUp(self):
        # Cria 10 cursos com o nome 'django'
        self.courses_django = mommy.make('courses.Course', name='Python com django', _quantity=10)
        # Cria 10 cursos com o nome 'web'
        self.courses_web = mommy.make('courses.Course', name='Python na web', _quantity=5)
        self.client = Client()

    # Método final executado após cada método da classe de testes
    def tearDown(self):
        Course.objects.all().delete()

    # Método para testar a função search do model de cursos
    def test_course_search(self):
        # Encontra os cursos com nome 'django' (deve retornar 10)
        search = Course.objects.search('django')
        self.assertEqual(len(search), 10)
        # Encontra os cursos com nome 'web' (deve retornar 5)
        search = Course.objects.search('web')
        self.assertEqual(len(search), 5)
        # Encontra os cursos com nome 'python'(deve retornar 15)
        search = Course.objects.search('Python')
        self.assertEqual(len(search), 15)
        # Encontra os cursos com nome 'python'(deve retornar 0)
        search = Course.objects.search('Django na web')
        self.assertEqual(len(search), 0)
