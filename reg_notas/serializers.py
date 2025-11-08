from rest_framework import serializers
from django.db import models
from .models import Estudiante, Asignatura, Matricula, MatriculasAsignatura, Nota, Evaluacion

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['id','nombre','appaterno']
        
class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = ['nombre']
        
class MatriculaSerializer(serializers.ModelSerializer):
    promedio = serializers.SerializerMethodField()

    class Meta:
        model = Matricula
        fields = '__all__'
    def get_promedio (self, obj):
        return round(obj.notas.aggregate(models.Avg('puntaje'))['puntaje__avg'] or 0,2)
        
class MatriculasAsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatriculasAsignatura
        fields = ['matricula', 'asignatura', 'year']
        
class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = ['evaluacion', 'matricula', 'puntaje']
        
        
class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = ['asignatura', 'nombre']
        



