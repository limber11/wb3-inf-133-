from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Manejador de solicitudes
class MiHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Ruta para obtener nombres que comienzan con la letra "P"
        if self.path == "/buscar_nombre":
            # Obtener la letra inicial del query string
            componentes_ruta = self.path.split("=")
            if len(componentes_ruta) >= 2:
                letra = componentes_ruta[1]
            else:
                # Manejar el caso en el que no hay '=' en la ruta
                self.send_response(400)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write("No se proporcionó la letra".encode())
                return
            # ... código para obtener los nombres ...
            nombres = ["Pedro", "Pablo", "Patricia"]
            # Responder con la lista de nombres en formato JSON
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(nombres).encode())
        else:
            # Responder con un mensaje de error
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write("Ruta no válida".encode())

# Creación e inicio del servidor
servidor = HTTPServer(("", 8000), MiHandler)
servidor.serve_forever()