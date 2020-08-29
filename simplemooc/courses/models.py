from django.db import models
from django.conf import settings

from simplemooc.core.mail import send_mail_template

class CourseManager(models.Manager):

    # Cria um novo método para o Manager do modelo Course
    def search(self, query):
        return self.get_queryset().filter(
            # Filtra com condicional OR
            models.Q(name__icontains=query) | models.Q(description__icontains=query)
            )

class Course(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição', blank=True)
    about = models.TextField('Sobre o curso', blank=True)
    start_date = models.DateField('Data de Início', null=True, blank=True)
    imagem = models.ImageField(upload_to='courses/images/', verbose_name='Imagem', null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    # Herda a classe Manager para obter os métodos criados
    objects = CourseManager()

    # Retorna a string a ser exibida no site
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.slug
        #return self.pk # Caso a link de url do curso esteja usando o código do curso e não a descrição

    # Configurações para exibição dos dados
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']

# Classe para as aulas do curso 
class Lesson(models.Model):
    name = models.CharField('Nome', max_length=100)
    descrition = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Número (ordem)', blank=True, default=0)
    release_date = models.DateField('Data de liberação', blank=True, null=True)
    course = models.ForeignKey(Course, verbose_name='Curso', related_name='lessons', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name =  'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']

# Classe para os materiais das aulas do curso 
class Material(models.Model):
    name = models.CharField('Nome', max_length=100)
    embedded = models.TextField('Vídeo embedded', blank=True)
    file = models.FileField(upload_to='lessons/materials', blank=True, null=True)
    lesson = models.ForeignKey(Lesson, verbose_name='Aula', related_name='materials', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name =  'Material'
        verbose_name_plural = 'Materiais'


# Classe para inscrição de usuários nos cursos
class Enrollment(models.Model):
    STATUS_CHOICE = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='Curso', related_name='enrollments', on_delete=models.CASCADE)
    status = models.IntegerField('Situação', choices=STATUS_CHOICE, default=0, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    # Ativa inscrição do usuário no curso
    def active(self):
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        # Define a relação entre usuário e curso. Só deve permitir 1:1 entre usuário e curso
        unique_together = (('user', 'course'))

class Announcement(models.Model):
    course = models.ForeignKey(Course, verbose_name='Curso', related_name='announcements', on_delete=models.CASCADE)
    title = models.CharField('TÍtulo', max_length=100)
    content = models.TextField('Conteúdo')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']

class Comment(models.Model):
    announcement = models.ForeignKey(Announcement, verbose_name='Anúncio', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
    comment = models.TextField('Comentário')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']

def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.title
        context = {
            'announcement': instance
        }
        template_name = 'courses/announcement_mail.html'
        enrollments = Enrollment.objects.filter(course=instance.course, status=1)
        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_mail_template(subject, template_name, context, recipient_list)

models.signals.post_save.connect(post_save_announcement, sender=Announcement, dispatch_uid='post_save_announcement')