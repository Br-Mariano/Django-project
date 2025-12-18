from django.contrib import admin
from .models import Usuario, Recordatorio, Libro, MiniRecordatorio

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'correo', 'nombre', 'creado_en')
    search_fields = ('usuario', 'correo', 'nombre')
    list_filter = ('creado_en',)

@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'hora', 'creado_en')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('hora', 'creado_en', 'usuario')

@admin.register(MiniRecordatorio)
class MiniRecordatorioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'hora', 'creado_en')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('hora', 'creado_en', 'usuario')
    
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'publicado_por', 'anio', 'genero', 'creado_en')
    search_fields = ('nombre', 'publicado_por', 'descripcion')
    list_filter = ('genero', 'creado_en', 'usuario')