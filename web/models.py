from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'usuarios'
    
    def __str__(self):
        return f"{self.usuario} ({self.correo})"
    
    def set_password(self, raw_password):
        self.contrasena = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.contrasena)


class Recordatorio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='recordatorios')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    hora = models.TimeField()
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'recordatorios'
        ordering = ['hora']
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.usuario}"


class Libro(models.Model):
    GENEROS = [
        ('ficcion', 'Ficción'),
        ('no_ficcion', 'No Ficción'),
        ('misterio', 'Misterio'),
        ('ciencia_ficcion', 'Ciencia Ficción'),
        ('romance', 'Romance'),
        ('otro', 'Otro'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='libros')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    publicado_por = models.CharField(max_length=200, blank=True)
    anio = models.CharField(max_length=4, blank=True)
    genero = models.CharField(max_length=20, choices=GENEROS, default='ficcion')
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'libros'
        ordering = ['-creado_en']
    
    def __str__(self):
        return f"{self.nombre} - {self.usuario.usuario}"