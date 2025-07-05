# Reimportar librerías tras reinicio del entorno
import json
import random
from datetime import datetime, timedelta

# Definir productos, vendedores y precios por unidad aproximados
productos = [
    ("Huevos", 0.2),
    ("Leche", 1.0),
    ("Queso", 2.5),
    ("Tomates", 0.8),
    ("Pollo", 5.0),
    ("Miel", 4.5),
    ("Manzanas", 0.7),
    ("Zanahorias", 0.6),
    ("Pan", 0.5),
    ("Arroz", 1.2),
    ("Papas", 0.4),
    ("Carne", 6.0),
    ("Yogur", 1.5),
    ("Harina", 0.9),
    ("Cereal", 3.0)
]

vendedores = ["Juan", "Ana", "Luis", "Maria", "Carlos"]

# Generar 365 fechas únicas para el año 2025
fecha_inicio = datetime.strptime("2025-01-01", "%Y-%m-%d")
fechas = [fecha_inicio + timedelta(days=i) for i in range(150)]

# Generar datos
datos = []
for fecha in fechas: 
    # entre 1 y 5 ventas por día
    for _ in range(random.randint(1, 5)): 
        producto, precio = random.choice(productos)
        datos.append({
            "producto": producto,
            "cantidadVendida": random.randint(5, 60),
            "precioUnitario": precio,
            "vendedor": random.choice(vendedores),
            "fecha": fecha.strftime("%Y-%m-%d")
        })

# Guardar el archivo
file_path = "../api/data/ventas.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(datos, f, indent=4)

print(f"Datos generados y guardados en {file_path}")
