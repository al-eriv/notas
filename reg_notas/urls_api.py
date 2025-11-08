from rest_framework.routers import DefaultRouter
from .views_api import (EstudianteViewSet, AsignaturaViewSet, MatriculaViewSet,
                        MatriculasAsignaturaViewSet, NotaViewSet, EvaluacionViewSet,
                        api_filtrar_notas, crear_estudiante, actualizar_estudiante, eliminar_estudiante,
                        crear_asignatura, editar_asignatura, eliminar_asignatura,
                        crear_matricula, editar_matricula, eliminar_matricula)
from django.urls import path

router = DefaultRouter()

router.register(r'estudiantes', EstudianteViewSet)
router.register(r'asignaturas', AsignaturaViewSet)
router.register(r'matriculas', MatriculaViewSet)
router.register(r'matriculas_asignaturas', MatriculasAsignaturaViewSet)
router.register(r'notas', NotaViewSet)
router.register(r'evaluaciones', EvaluacionViewSet)


urlpatterns = [
    path("api/notasfiltro/", api_filtrar_notas, name="api_filtrar_notas"),
    path("api/estudiantes/", crear_estudiante, name="crear_estudiante"),
    path("api/estudiantes/<int:pk>/", actualizar_estudiante, name="actualizar_estudiante"),
    path("api/estudiantes/<int:pk>/delete/", eliminar_estudiante, name="eliminar_estudiante"),
    path("api/crear-asignaturas/", crear_asignatura, name="crear_asignatura"),
    path("api/asignaturas/<int:pk>/", editar_asignatura, name="editar_asignatura"),
    path("api/asignaturas/<int:pk>/delete/", eliminar_asignatura, name="eliminar_asignatura"),
    path("api/matriculas-crea/", crear_matricula, name="crear_matricula"),
    path("api/matriculas/<int:pk>/", editar_matricula, name="editar_matricula"),
    path("api/matriculas/<int:pk>/delete", eliminar_matricula, name="eliminar_matricula"),
       
    
] + router.urls