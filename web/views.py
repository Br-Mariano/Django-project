from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Recordatorio, Libro
import json

def home(request):
    return render(request, 'web/index.html')

def main_page(request):
    return render(request, 'web/main_page.html')

def registro_libro(request):
    return render(request, 'web/registro_de_libro.html')

def get_cuenta_data(request):
    """Vista para obtener los datos del usuario actual de la sesión"""
    try:
        usuario_id = request.session.get('usuario_id')
        
        if not usuario_id:
            return JsonResponse({"status": "error", "mensaje": "No hay sesión activa"})
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            return JsonResponse({
                "usuario": usuario.usuario,
                "correo": usuario.correo
            })
        except Usuario.DoesNotExist:
            return JsonResponse({"status": "error", "mensaje": "Usuario no encontrado"})
            
    except Exception as e:
        return JsonResponse({"status": "error", "mensaje": str(e)})

@csrf_exempt
def guardar_json(request):
    """Maneja registro e inicio de sesión"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tipo = data.get("nombre", "data")

            if tipo == "cuentaData":
                # Registro de nuevo usuario
                correo = data.get("correo")
                
                # Verificar si el correo ya existe
                if Usuario.objects.filter(correo=correo).exists():
                    return JsonResponse({
                        "status": "error", 
                        "mensaje": "Este correo ya está registrado. Por favor, inicia sesión."
                    })

                # Crear nuevo usuario
                usuario = Usuario.objects.create(
                    nombre=data.get("usuario"),
                    usuario=data.get("usuario"),
                    correo=correo
                )
                usuario.set_password(data.get("contrasena"))
                usuario.save()

                # Guardar en sesión
                request.session['usuario_id'] = usuario.id
                return JsonResponse({"status": "ok", "mensaje": "Cuenta creada correctamente"})

            elif tipo == "loginData":
                # Inicio de sesión
                correo = data.get("correo")
                contrasena = data.get("contrasena")
                
                try:
                    usuario = Usuario.objects.get(correo=correo)
                    if usuario.check_password(contrasena):
                        request.session['usuario_id'] = usuario.id
                        return JsonResponse({
                            "status": "ok", 
                            "mensaje": "Inicio de sesión exitoso",
                            "usuario": usuario.usuario
                        })
                    else:
                        return JsonResponse({"status": "error", "mensaje": "Correo o contraseña incorrectos"})
                except Usuario.DoesNotExist:
                    return JsonResponse({"status": "error", "mensaje": "Correo o contraseña incorrectos"})

            else:
                return JsonResponse({"status": "error", "mensaje": "Tipo de dato desconocido"})

        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)})
    else:
        return JsonResponse({"status": "error", "mensaje": "Método no permitido"})


@csrf_exempt
def guardar_recordatorio(request):
    """Guardar un nuevo recordatorio para el usuario logueado"""
    if request.method == "POST":
        try:
            usuario_id = request.session.get('usuario_id')
            if not usuario_id:
                return JsonResponse({"status": "error", "mensaje": "No hay sesión activa"})
            
            try:
                usuario = Usuario.objects.get(id=usuario_id)
            except Usuario.DoesNotExist:
                return JsonResponse({"status": "error", "mensaje": "Usuario no encontrado"})
            
            data = json.loads(request.body)
            
            # Crear nuevo recordatorio
            recordatorio = Recordatorio.objects.create(
                usuario=usuario,
                titulo=data.get("titulo"),
                descripcion=data.get("descripcion", ""),
                hora=data.get("hora")
            )
            
            return JsonResponse({
                "status": "ok", 
                "mensaje": "Recordatorio guardado correctamente",
                "id": recordatorio.id
            })
            
        except Exception as e:
            print(f"Error en guardar_recordatorio: {str(e)}")
            return JsonResponse({"status": "error", "mensaje": str(e)})
    else:
        return JsonResponse({"status": "error", "mensaje": "Método no permitido"})


def obtener_recordatorios(request):
    """Obtener todos los recordatorios del usuario logueado"""
    try:
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return JsonResponse({"status": "error", "mensaje": "No hay sesión activa"})
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return JsonResponse({"status": "error", "mensaje": "Usuario no encontrado"})
        
        # Obtener recordatorios del usuario
        recordatorios = Recordatorio.objects.filter(usuario=usuario).order_by('hora')
        
        # Convertir a formato JSON
        agenda = []
        for rec in recordatorios:
            agenda.append({
                "id": str(rec.id),
                "titulo": rec.titulo,
                "descripcion": rec.descripcion,
                "hora": rec.hora.strftime('%H:%M')
            })
        
        # Obtener libros del usuario
        libros = Libro.objects.filter(usuario=usuario).order_by('-creado_en')
        
        biblioteca = []
        for libro in libros:
            biblioteca.append({
                "id": str(libro.id),
                "nombre": libro.nombre,
                "descripcion": libro.descripcion,
                "publicado_por": libro.publicado_por,
                "anio": libro.anio,
                "genero": libro.genero
            })
            
        return JsonResponse({
            "status": "ok", 
            "data": {
                "agenda": agenda,
                "biblioteca": biblioteca
            }
        })
        
    except Exception as e:
        print(f"Error en obtener_recordatorios: {str(e)}")
        return JsonResponse({"status": "error", "mensaje": str(e)})


@csrf_exempt
def editar_recordatorio(request):
    """Editar un recordatorio existente"""
    if request.method == "POST":
        try:
            usuario_id = request.session.get('usuario_id')
            if not usuario_id:
                return JsonResponse({"status": "error", "mensaje": "No hay sesión activa"})
            
            data = json.loads(request.body)
            recordatorio_id = data.get("id")
            
            try:
                recordatorio = Recordatorio.objects.get(id=recordatorio_id, usuario_id=usuario_id)
                recordatorio.titulo = data.get("titulo")
                recordatorio.descripcion = data.get("descripcion", "")
                recordatorio.hora = data.get("hora")
                recordatorio.save()
                
                return JsonResponse({"status": "ok", "mensaje": "Recordatorio actualizado"})
            except Recordatorio.DoesNotExist:
                return JsonResponse({"status": "error", "mensaje": "Recordatorio no encontrado"})
            
        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)})
    else:
        return JsonResponse({"status": "error", "mensaje": "Método no permitido"})


@csrf_exempt
def eliminar_recordatorio(request):
    """Eliminar un recordatorio"""
    if request.method == "POST":
        try:
            usuario_id = request.session.get('usuario_id')
            if not usuario_id:
                return JsonResponse({"status": "error", "mensaje": "No hay sesión activa"})
            
            data = json.loads(request.body)
            recordatorio_id = data.get("id")
            
            try:
                recordatorio = Recordatorio.objects.get(id=recordatorio_id, usuario_id=usuario_id)
                recordatorio.delete()
                return JsonResponse({"status": "ok", "mensaje": "Recordatorio eliminado"})
            except Recordatorio.DoesNotExist:
                return JsonResponse({"status": "error", "mensaje": "Recordatorio no encontrado"})
            
        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)})
    else:
        return JsonResponse({"status": "error", "mensaje": "Método no permitido"})


@csrf_exempt
def guardar_libro(request):
    """Guardar un nuevo libro para el usuario logueado"""
    if request.method == "POST":
        try:
            usuario_id = request.session.get('usuario_id')
            if not usuario_id:
                return JsonResponse({"status": "error", "mensaje": "No hay sesión activa"})
            
            try:
                usuario = Usuario.objects.get(id=usuario_id)
            except Usuario.DoesNotExist:
                return JsonResponse({"status": "error", "mensaje": "Usuario no encontrado"})
            
            data = json.loads(request.body)
            
            # Crear nuevo libro
            libro = Libro.objects.create(
                usuario=usuario,
                nombre=data.get("nombre"),
                descripcion=data.get("descripcion", ""),
                publicado_por=data.get("publicado_por", ""),
                anio=data.get("anio", ""),
                genero=data.get("genero", "ficcion")
            )
            
            return JsonResponse({"status": "ok", "mensaje": "Libro guardado correctamente"})
            
        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)})
    else:
        return JsonResponse({"status": "error", "mensaje": "Método no permitido"})


def obtener_libros(request):
    """Obtener todos los libros del usuario logueado"""
    try:
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return JsonResponse({"status": "error", "mensaje": "No hay sesión activa"})
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return JsonResponse({"status": "error", "mensaje": "Usuario no encontrado"})
        
        # Obtener libros del usuario
        libros = Libro.objects.filter(usuario=usuario).order_by('-creado_en')
        
        data = []
        for libro in libros:
            data.append({
                "id": str(libro.id),
                "nombre": libro.nombre,
                "descripcion": libro.descripcion,
                "publicado_por": libro.publicado_por,
                "anio": libro.anio,
                "genero": libro.genero
            })
        
        return JsonResponse({"status": "ok", "data": data})
        
    except Exception as e:
        return JsonResponse({"status": "error", "mensaje": str(e)})


@csrf_exempt
def eliminar_libro(request):
    """Eliminar un libro"""
    if request.method == "POST":
        try:
            usuario_id = request.session.get('usuario_id')
            if not usuario_id:
                return JsonResponse({"status": "error", "mensaje": "No hay sesión activa"})
            
            data = json.loads(request.body)
            libro_id = data.get("id")
            
            try:
                libro = Libro.objects.get(id=libro_id, usuario_id=usuario_id)
                libro.delete()
                return JsonResponse({"status": "ok", "mensaje": "Libro eliminado correctamente"})
            except Libro.DoesNotExist:
                return JsonResponse({"status": "error", "mensaje": "Libro no encontrado"})
            
        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)})
    else:
        return JsonResponse({"status": "error", "mensaje": "Método no permitido"})