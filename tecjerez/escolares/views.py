from django.http import JsonResponse  #Funcion para enviar respuestas enJSON
from django.forms.models import model_to_dict #Convierte de JSON a diccionario (python)
from django.views.decorators.csrf import csrf_exempt #Evita el bloqueo por CSRF

import json

from .models import Alumno # Para usar la tabla de mysql
from django.contrib.auth import authenticate, login # Vamos a usar la seguridad que nos brinda django
from django.contrib.auth.models import User # Importamos el modelo nativo


@csrf_exempt
def api_registro(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('usuario')
            password = data.get('password')

            # 1. Validar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': 'El nombre de usuario ya está ocupado.'}, status=400)

            # 2. Crear el usuario (create_user encripta el password automáticamente)
            user = User.objects.create_user(username=username, password=password)
            user.save()

            return JsonResponse({'status': 'success', 'message': 'Usuario creado correctamente'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('usuario')
            password = data.get('password')

            # revisa la tabla auth_user de MySQL
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user) # Crea la sesión en el navegador
                return JsonResponse({
                    'status': 'success',
                    'message': 'Bienvenido ' + user.username
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Usuario o contraseña incorrectos'
                }, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# Vista para Mostrar y crear
@csrf_exempt #Indica que no necesita de un token de seguridad (Para preubas)
def api_alumnos(request):
    if request.method == 'GET': #Consultas
        alumnos_queryset = Alumno.objects.all() #Hace la consulta de todos los alumnos
        alumnos_list = []
        
        for alumno in alumnos_queryset:
            item = model_to_dict(alumno)
            
            if item.get('fechaNac'):
                item['fechaNac'] = item['fechaNac'].isoformat() #Convertimos el objeto fecha a texto 
            alumnos_list.append(item)
            
        return JsonResponse(alumnos_list, safe=False) #Enviamos los aplumnos al frontend
    
    if request.method == 'POST': #Altas
        import json
        try:
            # Si el body está vacío, evitamos que truene
            if not request.body:
                return JsonResponse({'error': 'Cuerpo de petición vacío'}, status=400)
                
            data = json.loads(request.body)
            
            # Limpiamos el diccionario: si viene 'id' o 'alumno_id' vacío desde el modal de "Nuevo", 
            # lo quitamos para que MySQL genere uno nuevo automáticamente.
            data.pop('id', None)
            data.pop('alumno_id', None)
            
            alumno = Alumno.objects.create(**data)
            
            res_data = model_to_dict(alumno)
            if res_data.get('fechaNac') and not isinstance(res_data['fechaNac'], str):
                res_data['fechaNac'] = res_data['fechaNac'].isoformat()
                
            return JsonResponse(res_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# Vista para detalle, borrar y editar
@csrf_exempt
def api_alumno_detalle(request, pk):
    try:
        alumno = Alumno.objects.get(pk=pk)
    except Alumno.DoesNotExist:
        return JsonResponse({'error': 'No encontrado'}, status=404)
    
    if request.method == 'GET':
        data = model_to_dict(alumno)
        if data.get('fechaNac'):
            data['fechaNac'] = data['fechaNac'].isoformat()
        return JsonResponse(data)
    
    if request.method == 'DELETE':
        alumno.delete()
        return JsonResponse({'res': 'ok'})
    
    if request.method == 'PUT':
        import json
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(alumno, key, value)
        alumno.save()
        
        res_data = model_to_dict(alumno)
        # CORRECCIÓN AQUÍ: Solo formatear si NO es ya un string
        if res_data.get('fechaNac') and not isinstance(res_data['fechaNac'], str):
            res_data['fechaNac'] = res_data['fechaNac'].isoformat()
            
        return JsonResponse(res_data)