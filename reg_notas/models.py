from django.db import models

# Create your models here.
class Estudiante(models.Model):

    nombre = models.CharField(max_length=255)
    appaterno = models.CharField(max_length=255)
    class Meta:
        ordering = ['nombre']
    def __str__(self):
        return f"{self.nombre} {self.appaterno}"
        
class Asignatura(models.Model):
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.nombre}"


class Matricula(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete = models.CASCADE, related_name = 'matriculas')
    def __str__(self):
        return f"{self.estudiante}"
    
class MatriculasAsignatura(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name = 'asignaturas_inscritas')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name = 'matriculas')
    year = models.IntegerField()
    class Meta:
        unique_together = ('matricula', 'asignatura')
    def __str__(self):
        return f"{self.matricula} - {self.asignatura}"
@property
def promedio(self):
    return self.notas.aggregate(models.Avg('puntaje'))['puntaje__avg']
        
class Evaluacion(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name = 'evaluaciones_asignatura')
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.asignatura} - {self.nombre}"
    
class Nota(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='evaluaciones')
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name='notas')
    puntaje = models.IntegerField()
    
    class Meta:
        unique_together =('evaluacion', 'matricula')
        
        
