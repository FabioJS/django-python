from django import forms
from django.core.mail import send_mail
from django.conf import settings
from simplemooc.core.mail import send_mail_template

from .models import Comment

class ContactCourse(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(
        label='Mensagem/Dúvida', widget=forms.Textarea
    )

    # Função para enviar e-mail com dúvidas do curso
    def send_mail(self, course):
        subject = '[%s] - Contato' % course
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
        }
        template_name = 'courses/contact_email.html'
        send_mail_template(subject, template_name, context, [settings.DEFAULT_FROM_EMAIL])

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']