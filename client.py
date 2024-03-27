import requests
import json

url = "http://localhost:8000/products"
headers = {"Content-Type": "application/json"}

# POST /products
new_product_data = {
    "product_type": "tablet",
    "weight": 50,
    "flavor": "chocolate"
}
response = requests.post(url=url, json=new_product_data, headers=headers)
print(response.json())

new_product_data = {
    "product_type": "candy",
    "weight": 30,
    "flavor": "strawberry",
    "filling": "caramel"
}
response = requests.post(url=url, json=new_product_data, headers=headers)
print(response.json())

# GET /products
response = requests.get(url=url)
print(response.json())

# PUT /products/{product_id}
product_id_to_update = 1
updated_product_data = {
    "weight": 60,
    "flavor": "vanilla"
}
response = requests.put(f"{url}/{product_id_to_update}", json=updated_product_data, headers=headers)
print("Producto actualizado:", response.json())

# GET /products
response = requests.get(url=url)
print(response.json())

# DELETE /products/{product_id}
product_id_to_delete = 1
response = requests.delete(f"{url}/{product_id_to_delete}")
print("Producto eliminado:", response.json())

# GET /products
response = requests.get(url=url)
print(response.json())
