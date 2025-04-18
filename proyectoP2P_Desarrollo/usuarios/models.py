from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('prestamista', 'Prestamista'),
        ('prestatario', 'Prestatario'),
        ('admin', 'Administrador'),
    )
    
    ESTADOS = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('suspendido', 'Suspendido'),
    )
    
    rol = models.CharField(max_length=50, choices=ROLES)
    token_recuperacion = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    
    username = None
    email = models.EmailField('correo electrónico', unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'rol']
    
    class Meta:
        db_table = 'Usuario'
    
    def __str__(self):
        return self.email

class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    ingresos = models.DecimalField(max_digits=10, decimal_places=2)
    egresos = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.usuario.username

class HistorialCrediticio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación con el usuario
    score = models.IntegerField()  # Puntuación del historial crediticio
    reporte = models.TextField()   # Descripción del historial o notas del reporte
    fecha = models.DateField(auto_now_add=True)  # Fecha automática al crear el registro

    def __str__(self):
        return f'Historial de {self.usuario.username} - {self.score} en {self.fecha}'