# 🧭 Django Cheatsheet Express — Amuleto del Sábado

## 🔹 Comandos base
```bash
django-admin startproject myproject
python manage.py startapp myapp
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser
```

---

## 🔹 Estructura típica
```
myproject/
│ manage.py
│ myproject/settings.py
│ myproject/urls.py
│ myapp/models.py
│ myapp/views.py
│ myapp/templates/
```

---

## 🔹 Models y ORM
```python
from django.db import models

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    promedio = models.FloatField(default=0)
    activo = models.BooleanField(default=True)
```

### Crear / guardar
```python
e = Estudiante(nombre="Ana", promedio=5.5)
e.save()
Estudiante.objects.create(nombre="Luis", promedio=6.0)
```

### Leer
```python
Estudiante.objects.all()
Estudiante.objects.get(id=1)
Estudiante.objects.filter(promedio__gte=5)
```

### Actualizar
```python
Estudiante.objects.filter(id=1).update(promedio=6.5)
```

### Eliminar
```python
Estudiante.objects.filter(id=1).delete()
```

### Relaciones
```python
class Curso(models.Model):
    nombre = models.CharField(max_length=100)

class Matricula(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
```

### Consultas con relaciones
```python
Curso.objects.filter(matricula__estudiante__promedio__gt=5)
```

---

## 🔹 Views (function-based)
```python
from django.shortcuts import render, redirect
from .models import Estudiante

def lista_estudiantes(request):
    alumnos = Estudiante.objects.all()
    return render(request, "estudiantes.html", {"alumnos": alumnos})

def agregar_estudiante(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        Estudiante.objects.create(nombre=nombre)
        return redirect("lista_estudiantes")
    return render(request, "formulario.html")
```

---

## 🔹 Views (class-based)
```python
from django.views.generic import ListView, CreateView
from .models import Estudiante

class EstudianteListView(ListView):
    model = Estudiante
    template_name = "estudiantes.html"
    context_object_name = "alumnos"

class EstudianteCreateView(CreateView):
    model = Estudiante
    fields = ["nombre", "promedio"]
    template_name = "formulario.html"
    success_url = "/"
```

---

## 🔹 URLs
```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_estudiantes, name="lista_estudiantes"),
    path("agregar/", views.agregar_estudiante, name="agregar_estudiante"),
]
```

---

## 🔹 Templates
```html
<h1>Lista de estudiantes</h1>
<ul>
  {% for a in alumnos %}
    <li>{{ a.nombre }} — Promedio: {{ a.promedio }}</li>
  {% endfor %}
</ul>
```

---

## 🔹 Admin
```python
from django.contrib import admin
from .models import Estudiante

admin.site.register(Estudiante)
```

---

## 🔹 API y Serializers

### Crear una API básica con Django REST Framework
```python
# views.py
from rest_framework import viewsets
from .models import Estudiante
from .serializers import EstudianteSerializer

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
```

### Definir el Serializer
```python
# serializers.py
from rest_framework import serializers
from .models import Estudiante

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['id', 'nombre', 'promedio', 'activo']
```

### Registrar la API en urls.py
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudianteViewSet

router = DefaultRouter()
router.register(r'estudiantes', EstudianteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

### Ejemplo de Peticiones
- **GET** `/estudiantes/` → Lista todos los registros
- **POST** `/estudiantes/` → Crea un nuevo estudiante
- **GET** `/estudiantes/1/` → Detalle del estudiante con id=1
- **PUT/PATCH** `/estudiantes/1/` → Actualiza estudiante
- **DELETE** `/estudiantes/1/` → Elimina estudiante

---

## 🔹 Otros trucos rápidos

| Acción | Código |
|--------|--------|
| Contar registros | `Estudiante.objects.count()` |
| Ordenar | `Estudiante.objects.order_by('-promedio')` |
| Evitar duplicados | `.distinct()` |
| Limitar resultados | `.all()[:5]` |
| Buscar parcial | `.filter(nombre__icontains="an")` |
| Excluir | `.exclude(activo=False)` |

---

## 💡 Recordatorio final
- ORM → *Habla con la base sin SQL*  
- Vistas → *Reciben request, devuelven respuesta*  
- Templates → *HTML + variables*  
- API → *Django REST Framework simplifica el CRUD*  
- `urls.py` → *Tu mapa de rutas*  
- Si dudás: buscá “palabra + Django docs” y llegás más rápido que improvisando.

---

## 🧱 Middleware y settings básicos
```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'myapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]
```

---

## 🗝️ Autenticación rápida (login/logout)
```python
from django.contrib.auth import authenticate, login, logout

user = authenticate(request, username='ali', password='1234')
if user is not None:
    login(request, user)
else:
    # error de login

logout(request)
```

---

## 🪶 Resumen ultra rápido del ciclo Django
```
Request → URL → View → (Model) → Template → Response
```

Comando útil para pruebas:
```bash
python manage.py shell
```
