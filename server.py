from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Base de datos simulada de productos
products = {}


class Product:
    def __init__(self, product_type, weight, flavor, filling=None):
        self.product_type = product_type
        self.weight = weight
        self.flavor = flavor
        self.filling = filling


class Tablet(Product):
    def __init__(self, weight, flavor):
        super().__init__("tablet", weight, flavor)


class Candy(Product):
    def __init__(self, weight, flavor, filling):
        super().__init__("candy", weight, flavor, filling)


class Truffle(Product):
    def __init__(self, weight, flavor, filling):
        super().__init__("truffle", weight, flavor, filling)


class ProductFactory:
    @staticmethod
    def create_product(product_type, weight, flavor, filling=None):
        if product_type == "tablet":
            return Tablet(weight, flavor)
        elif product_type == "candy":
            return Candy(weight, flavor, filling)
        elif product_type == "truffle":
            return Truffle(weight, flavor, filling)
        else:
            raise ValueError("Tipo de producto no válido")


class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


class ProductService:
    def __init__(self):
        self.factory = ProductFactory()

    def add_product(self, data):
        product_type = data.get("product_type", None)
        weight = data.get("weight", None)
        flavor = data.get("flavor", None)
        filling = data.get("filling", None) if product_type in ["candy", "truffle"] else None

        product = self.factory.create_product(
            product_type, weight, flavor, filling
        )
        products[len(products) + 1] = product
        return product

    def list_products(self):
        return {index: product.__dict__ for index, product in products.items()}

    def update_product(self, product_id, data):
        if product_id in products:
            product = products[product_id]
            weight = data.get("weight", None)
            flavor = data.get("flavor", None)
            filling = data.get("filling", None) if product.product_type in ["candy", "truffle"] else None

            if weight:
                product.weight = weight
            if flavor:
                product.flavor = flavor
            if filling:
                product.filling = filling
            return product
        else:
            raise None

    def delete_product(self, product_id):
        if product_id in products:
            del products[product_id]
            return {"message": "Producto eliminado"}
        else:
            return None


class ProductRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.product_service = ProductService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/products":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.product_service.add_product(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_GET(self):
        if self.path == "/products":
            response_data = self.product_service.list_products()
            HTTPDataHandler.handle_response(self, 200, response_data)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_PUT(self):
        if self.path.startswith("/products/"):
            product_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.product_service.update_product(product_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Producto no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_DELETE(self):
        if self.path.startswith("/products/"):
            product_id = int(self.path.split("/")[-1])
            response_data = self.product_service.delete_product(product_id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Producto no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, ProductRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()
