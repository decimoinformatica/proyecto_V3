from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import RegistroForm, LoginForm
from .form_perfil import PerfilForm
import random
from datetime import date
from .models import Perfil, HistorialCrediticio

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('crear_perfil')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Autentica usando el email como username
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('ver_perfil')
        else:
            return render(request, 'usuarios/login.html', {
                'error': 'Correo o contraseña incorrectos'
            })
    return render(request, 'usuarios/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'usuarios/dashboard.html', {'user': request.user})

'''
@login_required
def crear_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()
            return redirect('dashboard')  # Cambia esto al nombre correcto de tu dashboard
    else:
        form = PerfilForm()
    return render(request, 'perfil/crear_perfil.html', {'form': form})
'''

# Función para generar una fecha aleatoria entre los años 2015 y 2025
def generar_fecha_aleatoria():
    # Definir el rango de años
    start_year = 2015
    end_year = 2025

    # Generar un año aleatorio en ese rango
    year = random.randint(start_year, end_year)
    
    # Generar un mes y día aleatorio
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Para evitar problemas con los días fuera de rango

    # Crear una fecha aleatoria
    return date(year, month, day)

# Función para crear el historial crediticio con datos aleatorios
def crear_historial(usuario):
    for _ in range(10):
        # Generar puntaje aleatorio entre 5 y 10
        score = random.randint(5, 10)
        
        # Generar un reporte aleatorio con las opciones predefinidas
        opciones_reporte = ['nuevo', 'en proceso', 'finalizado']
        reporte = random.choice(opciones_reporte)
        
        # Generar una fecha aleatoria entre los años 2015 y 2025
        fecha_aleatoria = generar_fecha_aleatoria()
        
        # Crear historial crediticio con los datos generados
        historial = HistorialCrediticio(
            usuario=usuario,
            score=score,
            reporte=reporte,
            fecha=fecha_aleatoria,
        )
        historial.save()

@login_required
def crear_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()

            # Llamar a la función para crear los 10 registros de historial crediticio
            crear_historial(perfil.usuario)

            return redirect('ver_perfil')  # Redirige al dashboard después de crear el perfil y los registros
    else:
        form = PerfilForm()

    return render(request, 'perfil/crear_perfil.html', {'form': form})

@login_required
def ver_perfil(request):
    try:
        # Obtener el perfil del usuario actual
        perfil = Perfil.objects.get(usuario=request.user)

        # Obtener el nombre y apellido desde el modelo User
        nombre_completo = f"{request.user.first_name} {request.user.last_name}" if request.user.first_name and request.user.last_name else "Nombre no disponible"

        # Obtener el historial crediticio asociado al perfil
        historial_crediticio = HistorialCrediticio.objects.filter(usuario=perfil.usuario)
    except Perfil.DoesNotExist:
        perfil = None
        historial_crediticio = []
        nombre_completo = "Nombre no disponible"
        print("Perfil no encontrado para el usuario.")

    return render(request, 'perfil/ver_perfil.html', {
        'perfil': perfil,
        'historial_crediticio': historial_crediticio,
        'nombre_completo': nombre_completo,
    })
@login_required
def editar_perfil(request):
    perfil = Perfil.objects.get(usuario=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('ver_perfil')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'perfil/editar_perfil.html', {'form': form})