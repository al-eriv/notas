from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, filters, status
from .models import Estudiante, Asignatura, Matricula, MatriculasAsignatura, Nota, Evaluacion
from .serializers import (EstudianteSerializer, AsignaturaSerializer, 
                          MatriculaSerializer, MatriculasAsignaturaSerializer, 
                          NotaSerializer, EvaluacionSerializer)

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre','appaterno']
    ordering_fields = ['appaterno']
    
class AsignaturaViewSet(viewsets.ModelViewSet):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']
    
class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    
class MatriculasAsignaturaViewSet(viewsets.ModelViewSet):
    queryset = MatriculasAsignatura.objects.all()
    serializer_class = MatriculasAsignaturaSerializer
    
class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    
class EvaluacionViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    

@api_view(["GET"])
def api_filtrar_notas(request):
    estudiante = request.GET.get('estudiante')
    min_puntaje = request.GET.get('min')
    max_puntaje = request.GET.get('max')
    
    query = Q()
    if estudiante:
        query &= Q(matricula__estudiante__nombre__icontains=estudiante)
    if min_puntaje:
        query &= Q(puntaje__gte = int(min_puntaje))
    if max_puntaje:
        query &= Q(puntaje__lte = int(max_puntaje))
    
    notas = Nota.objects.filter(query).select_related("evaluacion","matricula__estudiante")
    
    if not notas.exists():
        return Response({"detalle":"No hay notas con esos parámetros"},
           status=status.HTTP_404_NOT_FOUND,
           )
        
    serializer = NotaSerializer(notas, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def api_crear_nota(request):
    serializer = NotaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def crear_estudiante(request):
    serializer = EstudianteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT","PATCH"])
def actualizar_estudiante(request, pk):
    try:
        estudiante = Estudiante.objects.get(pk=pk)
    except Estudiante.DoesNotExist:
        return Response({"error":"No encontrado"},
                        status= status.HTTP_404_NOT_FOUND)
    
    serializer = Estudiante(estudiante, data=request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
@api_view(["DELETE"])
def eliminar_estudiante(request, pk):
    try:
        estudiante = Estudiante.objects.get(pk=pk)
        estudiante.delete()
        return Response({"mensaje": "Estudiante eliminado"}, status=status.HTTP_204_NO_CONTENT)
    except Estudiante.DoesNotExist:
        return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        
@api_view(["POST"])
def crear_asignatura(request):
    serializer = AsignaturaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT","PATCH"])
def editar_asignatura(request,pk):
    try:
        asignatura = Asignatura.objects.get(pk=pk)
    except Asignatura.DoesNotExist:
        return Response({"error":"asignatura no encontrada"}, status =status.HTTP_404_NOT_FOUND)
    
    serializer = AsignaturaSerializer(asignatura, data=request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def eliminar_asignatura(request, pk):
    try:
        asignatura = Asignatura.objects.get(pk=pk)
        asignatura.delete()
        return Response({"mensaje":"Asignatura Eliminada"}, status=status.HTTP_204_NO_CONTENT)
    
    except Asignatura.DoesNotExist:
        return Response({"error":"asignatura no encontrada"})
    

    
@api_view(["POST"])
def crear_matricula(request):
    serializer = MatriculasAsignaturaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT","PATCH"])
def editar_matricula(request,pk):
    try:
        matricula = Matricula.objects.get(pk=pk)
    except Matricula.DoesNotExist:
        return Response({"error":"Matricula no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    serializer = MatriculaSerializer(matricula, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def eliminar_matricula(request,pk):
    try:
        matricula = Matricula.objects.get(pk=pk)
        matricula.delete()
        return Response({"mensaje":"Matricula eliminada."}, status=status.HTTP_204_NO_CONTENT)
    except Matricula.DoesNotExist:
        return Response({"error":"Matricula no encontrada"}, status=status.HTTP_400_BAD_REQUEST)

