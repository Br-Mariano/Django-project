from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('guardar-json/', views.guardar_json, name='guardar_json'),
    path('main_page/', views.main_page, name='main_page'),
    path('api/cuenta-data/', views.get_cuenta_data, name='get_cuenta_data'),
    path('registro_libro/', views.registro_libro, name='registro_libro'),
    path('api/recordatorios/', views.obtener_recordatorios, name='obtener_recordatorios'),
    path('api/recordatorios/guardar/', views.guardar_recordatorio, name='guardar_recordatorio'),
    path('api/recordatorios/editar/', views.editar_recordatorio, name='editar_recordatorio'),
    path('api/recordatorios/eliminar/', views.eliminar_recordatorio, name='eliminar_recordatorio'),
    path('api/mini-recordatorios/', views.obtener_mini_recordatorios, name='obtener_mini_recordatorios'),
    path('api/mini-recordatorios/guardar/', views.guardar_mini_recordatorio, name='guardar_mini_recordatorio'),
    path('api/mini-recordatorios/editar/', views.editar_mini_recordatorio, name='editar_mini_recordatorio'),
    path('api/mini-recordatorios/eliminar/', views.eliminar_mini_recordatorio, name='eliminar_mini_recordatorio'),
    path('guardar_libro/', views.guardar_libro, name='guardar_libro'),
    path('obtener_libros/', views.obtener_libros, name='obtener_libros'),
    path('eliminar_libro/', views.eliminar_libro, name='eliminar_libro'),
]