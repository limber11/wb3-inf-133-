from http.server import HTTPServer, BaseHTTPRequestHandler
import json

estudiantes = [
    {
        "id": 1,
        "nombre": "Pedrito",
        "apellido": "García",
        "carrera": "Ingeniería de Sistemas",
    },
    {
        "id": 2,
        "nombre": "Limber",
        "apellido": "Lucia",
        "carrera": "Turismo",
    },
    {
        "id": 3,
        "nombre": "Ana",
        "apellido": "López",
        "carrera": "Economía",
    },
    {
        "id": 4,
        "nombre": "Juan",
        "apellido": "Pérez",
        "carrera": "Economía",
    },
]

carreras = {
    "Ingeniería de Sistemas": [estudiantes[0]],
    "Economía": [estudiantes[2], estudiantes[3]],
    "Turismo": [estudiantes[1]],
}

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/carreras":
            # Get all careers
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(list(carreras.keys())).encode("utf-8"))
        elif self.path.startswith("/carreras/"):
            carrera_nombre = self.path.split("/")[-1]
            if carrera_nombre in carreras:
                # Get students by career
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(carreras[carrera_nombre]).encode("utf-8"))
            else:
                # Career not found
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"Error": "Carrera no encontrada"}).encode("utf-8"))
        else:
            # Route not found
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"Error": "Ruta no encontrada"}).encode("utf-8"))

    def do_POST(self):
        if self.path == "/estudiantes":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode("utf-8"))

            # Check for required fields and validity (can be extended for additional checks)
            if not all(field in post_data for field in ["nombre", "apellido", "carrera"]):
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"Error": "Campos faltantes o inválidos"}).encode("utf-8"))
                return  # Exit early on error

            # Assign unique ID and add student
            post_data["id"] = len(estudiantes) + 1
            estudiantes.append(post_data)
            carreras.setdefault(post_data["carrera"], []).append(post_data)  # Add to career list

            self.send_response(201)  # Created
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(post_data).encode("utf-8"))
        else:
            # Route not found
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"Error": "Ruta no encontrada"}).encode("utf-8"))

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()
        
if __name__ == "__main__":
    run_server()