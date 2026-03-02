![Django CI](https://github.com/SebasPlata/article-manager/actions/workflows/django-ci.yml/badge.svg)
# Guía Completa para Crear y Configurar un Article Manager en Django

**Tipo de presentación:** Documento técnico en Markdown publicado en
repositorio GitHub público.

------------------------------------------------------------------------

## 0. Creación de un ambiente virtual para trabajar en Django

### Paso 1: Instalar Python

Descargar Python desde: https://www.python.org/downloads/

Verificar instalación:

``` bash
python --version
```

### Paso 2: Crear entorno virtual

``` bash
python -m venv venv
```

Activar entorno virtual (Windows):

``` bash
venv\Scripts\activate
```

Si todo está correcto, aparecerá `(venv)` en la terminal.

### Paso 3: Instalar Django y librerías necesarias

``` bash
pip install django
pip install django-extensions
```

Guardar dependencias:

``` bash
pip freeze > requirements.txt
```

------------------------------------------------------------------------

## 1. Pasos para crear un proyecto en Django (incluye base de datos)

### Paso 1: Crear carpeta y abrir terminal

1.  Crear carpeta del proyecto (ej. ArticleManager).
2.  Abrir terminal dentro de esa carpeta.

### Paso 2: Crear el proyecto

``` bash
django-admin startproject config .
```

Archivos principales creados: - manage.py - Carpeta config/

### Paso 3: Configurar base de datos

En `config/settings.py` buscar `DATABASES`.

#### SQLite (por defecto)

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### SQL Server (ejemplo)

``` python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'nombre_db',
        'USER': 'usuario',
        'PASSWORD': 'password',
        'HOST': 'localhost',
    }
}
```

### Paso 4: Ejecutar migraciones iniciales

``` bash
python manage.py migrate
```

------------------------------------------------------------------------

## 2. Pasos para crear una app en Django (incluye settings)

### Paso 1: Crear la app

``` bash
python manage.py startapp articles
```

### Paso 2: Registrar la app

En `config/settings.py` agregar en `INSTALLED_APPS`:

``` python
'articles',
'django_extensions',
```

### Paso 3: Crear modelo

En `articles/models.py`:

``` python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title
```

### Paso 4: Crear migraciones

``` bash
python manage.py makemigrations
python manage.py migrate
```

------------------------------------------------------------------------

## 3. Estructura de archivos

``` text
project/
├─ manage.py
├─ requirements.txt
├─ config/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ asgi.py
└─ articles/
   ├─ models.py
   ├─ views.py
   ├─ forms.py
   ├─ urls.py
   ├─ scripts/
   │  └─ populate_articles.py
   ├─ templates/
   │  ├─ article_template.html
   │  └─ article_form.html
   └─ migrations/
```

------------------------------------------------------------------------

## 4. Probar modificaciones

Si se modifica modelo:

``` bash
python manage.py makemigrations
python manage.py migrate
```

Correr servidor:

``` bash
python manage.py runserver
```

Abrir en navegador:

http://127.0.0.1:8000/

------------------------------------------------------------------------

## 5. URL para mostrar todas las entidades

### Vista en views.py

``` python
from django.shortcuts import render
from .models import Article

def article_list(request):
    articles = Article.objects.all().order_by('-id')
    return render(request, 'article_template.html', {'articles': articles})
```

### articles/urls.py

``` python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
]
```

### config/urls.py

``` python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('articles.urls')),
]
```

### Template article_template.html

``` html
<h1>Lista de Artículos</h1>

<p><a href="/create/">Crear nuevo artículo</a></p>

{% for article in articles %}
  <hr>
  <h2>{{ article.title }}</h2>
  <p>{{ article.content }}</p>
{% empty %}
  <p>No hay artículos todavía.</p>
{% endfor %}
```

------------------------------------------------------------------------

## 6. URL para crear nueva entidad

### forms.py

``` python
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
```

### Vista en views.py

``` python
from django.shortcuts import render, redirect
from .forms import ArticleForm

def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm()

    return render(request, 'article_form.html', {'form': form})
```

### Agregar ruta

``` python
path('create/', views.article_create, name='article_create'),
```

### Template article_form.html

``` html
<h1>Nuevo Artículo</h1>

<form method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Guardar</button>
</form>

<p><a href="/">Volver a la lista</a></p>
```

------------------------------------------------------------------------

## Extra: Carga masiva desde CSV

``` bash
python manage.py runscript populate_articles --script-args "articles/data/articles.csv"
```

Con limpieza previa:

``` bash
python manage.py runscript populate_articles --script-args "articles/data/articles.csv" "clear"
```

------------------------------------------------------------------------

## Referencias

-   https://docs.djangoproject.com/
-   https://docs.python.org/

Documento elaborado con fines académicos.
