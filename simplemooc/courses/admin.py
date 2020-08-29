from django.contrib import admin

from .models import (Course, Enrollment, Announcement, Comment, Lesson, Material)

class CourseAdmin(admin.ModelAdmin):
    # Campos a serem exibidos
    list_display = ['name', 'slug', 'start_date', 'created_at']
    # Campos que poderão ser pesquisados
    search_fields = ['name', 'slug']
    # Campos a serem pré-carregados a partir de outros
    prepopulated_fields = {'slug': ('name',)}

class MaterialInlineAdmin(admin.StackedInline):
    model = Material

class LessonAdmin(admin.ModelAdmin):
    # Campos a serem exibidos
    list_display = ['name', 'number', 'course', 'release_date']
    # Campos que poderão ser pesquisados
    search_fields = ['name', 'description']
    # Lista de campos a serem adicionados ao filtro lateral
    list_filter = ['created_at']
    inlines = [MaterialInlineAdmin]

# Indica que permite o Admin registrar cursos
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register([Enrollment, Announcement, Comment])
