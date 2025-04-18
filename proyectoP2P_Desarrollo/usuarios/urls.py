from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('crear-perfil/', views.crear_perfil, name='crear_perfil'),
    path('ver-perfil/', views.ver_perfil, name='ver_perfil'), 
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
]