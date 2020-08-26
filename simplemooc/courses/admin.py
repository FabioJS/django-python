from django.contrib import admin

from .models import Course, Enrollment, Announcement, Comment

class CourseAdmin(admin.ModelAdmin):
    # Campos a serem exibidos
    list_display = ['name', 'slug', 'start_date', 'created_at']
    # Campos que poderão ser pesquisados
    search_fields = ['name', 'slug']
    # Campos a serem pré-carregados a partir de outros
    prepopulated_fields = {'slug': ('name',)}

# Indica que permite o Admin registrar cursos
admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment])