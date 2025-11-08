from django.contrib import admin

from .models import Estudiante, Asignatura, Matricula, MatriculasAsignatura, Nota, Evaluacion

admin.site.register(Estudiante)
admin.site.register(Asignatura)
admin.site.register(Matricula)
admin.site.register(MatriculasAsignatura)
admin.site.register(Evaluacion)


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('evaluacion', 'matricula', 'puntaje')
    search_fields = ('matricula', 'id_estudiante', 'nombre')
