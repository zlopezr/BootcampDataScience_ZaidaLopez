# SportRetail LAM — API de Datos para Business Case

> Este README incluye información del API mock y también sirve como resumen de entrega para el taller.

## Entrega principal
- Notebook para entregar: `SportRetail_API_Analisis.ipynb`
- Carpeta `output` con los archivos exportados:
  - archivos `.csv`
  - archivo Power BI: `SPORT_RETAIL_LAM.pbix`

## Material adicional incluido
- El documento de instalación de la API se encuentra en `DS_TechnicalAssessment_Candidate.docx`.
- `sportretail_lam_api_f.zip` es la API original comprimida.
- En la carpeta original `sportretail_lam_api_f` está el trabajo de extracción de la API, el notebook utilizado y los archivos de salida.

##  Objetivo del taller
El objetivo de este taller es integrar la consulta de datos desde APIs usando Python con la construcción de reportes en Power BI.

### Actividad realizada
- Consulta a una API simulada desde Python.
- Transformación y limpieza de datos.
- Generación de dataset final listo para análisis.
- Exportación de los datos a `.csv`.
- Construcción de un reporte Power BI en `output/SPORT_RETAIL_LAM.pbix`.

---

##  Setup rápido de API local

```bash
# 1. Instalar dependencias
pip install fastapi uvicorn faker

# 2. Generar los datos dummy
python generate_data.py

# 3. Levantar el servidor
python api_server.py
# → http://localhost:8000
# → Docs interactivas: http://localhost:8000/docs
```

---

##  Endpoints disponibles

### Productos
| Método | Endpoint | Parámetros opcionales |
|--------|----------|-----------------------|
| GET | `/products` | `limit`, `skip`, `category`, `brand` |
| GET | `/products/{id}` | — |
| GET | `/products/categories/list` | — |

### Usuarios (Retailers)
| Método | Endpoint | Parámetros opcionales |
|--------|----------|-----------------------|
| GET | `/users` | `limit`, `skip`, `country`, `retailerType` |
| GET | `/users/{id}` | — |
| GET | `/users/{id}/carts` | — |

### Órdenes
| Método | Endpoint | Parámetros opcionales |
|--------|----------|-----------------------|
| GET | `/carts` | `limit`, `skip`, `userId`, `status`, `channel` |
| GET | `/carts/{id}` | — |

### Utilidades
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Estado del servidor y conteo de registros |

---

##  Estructura de respuestas

### `/products`
```json
{
  "total": 120, "skip": 0, "limit": 30, "count": 30,
  "products": [
    {
      "id": 1,
      "title": "SpeedMax Running Shoes v1",
      "category": "Footwear",
      "brand": "SpeedMax",
      "price": 142.50,
      "discountPercentage": 12.3,
      "stock": 340,
      "rating": 4.2,
      "reviews": 215,
      "sku": "SR-FOO-0001"
    }
  ]
}
```

### `/users`
```json
{
  "total": 100, "skip": 0, "limit": 30, "count": 30,
  "users": [
    {
      "id": 1,
      "firstName": "Valentina",
      "lastName": "Herrera",
      "email": "v.herrera@tiendamax.co",
      "age": 34,
      "country": "Colombia",
      "city": "Medellín",
      "phone": "+57 310 555 0192",
      "address": "Calle 80 # 45-12",
      "retailerType": "Sports Chain"
    }
  ]
}
```

### `/carts`
```json
{
  "total": 200, "skip": 0, "limit": 30, "count": 30,
  "carts": [
    {
      "id": 1,
      "userId": 23,
      "totalProducts": 3,
      "orderDate": "2024-03-15",
      "status": "delivered",
      "channel": "Direct Sales",
      "products": [
        {
          "id": 5,
          "title": "CoreFit Training Shoes v2",
          "price": 89.99,
          "quantity": 48,
          "category": "Footwear",
          "discountPercentage": 8.5
        }
      ]
    }
  ]
}
```

---

##  Ejemplos de llamadas

```python
import requests

BASE = "http://localhost:8000"

# Todos los productos de Footwear
r = requests.get(f"{BASE}/products", params={"category": "Footwear", "limit": 100})
products = r.json()["products"]

# Usuarios de Colombia
r = requests.get(f"{BASE}/users", params={"country": "Colombia", "limit": 100})
users = r.json()["users"]

# Todas las órdenes entregadas
r = requests.get(f"{BASE}/carts", params={"status": "delivered", "limit": 200})
orders = r.json()["carts"]
```

---

## 📝 Notas de calidad de datos

Los datos contienen **intencionalmente** algunos problemas para evaluar habilidades de limpieza:
- ~4% de productos tienen `stock: null`
- ~3% de productos tienen `rating: null`
- ~3% de usuarios tienen `email: null`
- ~2% de líneas de orden tienen `quantity: null`
- ~3 productos duplicados en el catálogo

El candidato debe documentar cómo detectó y resolvió cada uno.
