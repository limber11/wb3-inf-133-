import requests

# URL base del servidor
url = "http://localhost:8000/"

# Rutas adaptadas a la nueva estructura del servidor
ruta_carreras = url + "carreras"
ruta_carrera_id = url + "carreras/{}"
ruta_estudiantes = url + "estudiantes"

# Diccionario con datos de un nuevo estudiante
nuevo_estudiante = {
    "nombre": "Juanito",
    "apellido": "Pérez",
    "carrera": "Ingeniería Agronómica",
}

# ID de la carrera a consultar
id_carrera = "Ingeniería de Sistemas"

# Peticiones HTTP adaptadas
# GET: Obtener todas las carreras
get_carreras_response = requests.get(ruta_carreras)
print(f"GET /carreras: {get_carreras_response.text}")

# GET: Obtener estudiantes de una carrera
get_carrera_id_response = requests.get(ruta_carrera_id.format(id_carrera))
print(f"GET /carreras/{id_carrera}: {get_carrera_id_response.text}")

# POST: Agregar un nuevo estudiante (no ha cambiado)
post_response = requests.post(ruta_estudiantes, json=nuevo_estudiante)
print(f"POST /estudiantes: {post_response.text}")