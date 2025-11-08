from django.shortcuts import render, HttpResponse
from .models import Nota, Evaluacion, Matricula, Estudiante
from django.db.models import Q

def crear_nota(request):
    if request.method == "POST":
        evaluacion_id = request.POST.get("evaluacion")
        matricula_id = request.POST.get("matricula")
        puntaje = request.POST.get("puntaje")
        
        Nota.objects.create(
            evaluacion_id = evaluacion_id,
            matricula_id = matricula_id,
            puntaje = puntaje
        )
        
    evaluaciones = Evaluacion.objects.all()
    matriculas = Matricula.objects.all()
        
    return render(request, "reg_notas/form_nota.html", {
        "evaluaciones": evaluaciones,
        "matriculas": matriculas,
    })
    
def mostrar_notas(request):
    notas = None
    matriculas = Matricula.objects.select_related('estudiante')
    
    if request.method == "POST":
        matricula_id = request.POST.get("matricula")
        notas = Nota.objects.filter(matricula_id=matricula_id).select_related('evaluacion__asignatura')
    
    return render(request, "reg_notas/ver_notas.html", {
        "matriculas": matriculas,
        "notas": notas,
    })


def lista_notas(request):
    notas = Nota.objects.all()
    if not notas.exists():
        return HttpResponse('No hay notas registradas.')
    
    lineas = []
    for n in notas:
        asignatura = n.evaluacion.nombre
        matricula = n.matricula.estudiante.nombre
        lineas.append(f"{matricula} - {asignatura}: {n.puntaje} ")
    return HttpResponse('<br>'.join(lineas))


def filtrar_notas(request):
    lineas = []
    
    nombre_estudiante = request.GET.get('estudiante')
    notas = Nota.objects.filter(matricula__estudiante__nombre__icontains=nombre_estudiante)
        
    if not notas.exists():
        return HttpResponse('No hay notas registradas.')
    
    for nota in notas:
        evaluacion = nota.evaluacion.nombre
        puntaje = nota.puntaje
        lineas.append(f"{evaluacion}: {puntaje}")
    
    return HttpResponse('<br>'.join(lineas))

def filtrar_notas_avanzado(request):
    lineas = []
    nombre_estudiante = request.GET.get('estudiante')
    nota_min = request.GET.get('min')
    nota_max = request.GET.get('max')
    
    query = Q()
    if nombre_estudiante:
        query &= Q(matricula__estudiante__nombre__icontains=nombre_estudiante)
    if nota_min:
        query &= Q(puntaje__gte = int(nota_min))
    if nota_max:
        query &= Q(puntaje__lte = int(nota_max))
    
    notas = Nota.objects.filter(query).select_related("evaluacion","matricula__estudiante")
    
    if not notas.exists():
        return HttpResponse('No hay notas con esos parámetros.')
    
    for nota in notas:
        evaluacion = nota.evaluacion.nombre
        puntaje = nota.puntaje
        lineas.append(f"{evaluacion}: {puntaje}")
    
    return HttpResponse('<br>'.join(lineas))
    
