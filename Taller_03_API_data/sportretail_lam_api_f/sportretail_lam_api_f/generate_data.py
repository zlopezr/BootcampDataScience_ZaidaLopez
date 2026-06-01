"""
SportRetail LAM — Generador de Datos Dummy
Genera productos, usuarios y órdenes con contexto wholesale de sportswear LAM.
"""

import random
import json
from faker import Faker
from pathlib import Path

random.seed(42)

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
COUNTRIES = ["Colombia", "México", "Argentina", "Chile", "Perú"]
COUNTRY_CITIES = {
    "Colombia":  ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena"],
    "México":    ["Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Tijuana"],
    "Argentina": ["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "Tucumán"],
    "Chile":     ["Santiago", "Valparaíso", "Concepción", "Antofagasta", "Temuco"],
    "Perú":      ["Lima", "Arequipa", "Trujillo", "Cusco", "Piura"],
}

CATEGORIES = {
    "Footwear":      ["Running Shoes", "Basketball Shoes", "Training Shoes", "Slides", "Football Boots", "Tennis Shoes"],
    "Apparel":       ["Performance T-Shirt", "Training Shorts", "Track Jacket", "Compression Tights", "Football Jersey", "Sports Bra"],
    "Accessories":   ["Sport Backpack", "Water Bottle", "Cap", "Headband", "Gym Bag", "Sport Socks"],
    "Equipment":     ["Resistance Bands", "Jump Rope", "Yoga Mat", "Foam Roller", "Training Gloves", "Agility Ladder"],
    "Team Sports":   ["Football", "Basketball", "Volleyball", "Tennis Racket", "Goalkeeper Gloves", "Shin Guards"],
}

PRICE_RANGES = {
    "Footwear":    (55,  280),
    "Apparel":     (20,  130),
    "Accessories": (10,   90),
    "Equipment":   (15,  110),
    "Team Sports": (12,  160),
}

BRANDS = ["SportRetail Pro", "AthletX", "CoreFit", "SpeedMax", "UrbanSport", "PowerEdge"]

fakers = {c: Faker(["es_CO","es_MX","es_AR","es_CL","es_ES"][i]) for i,c in enumerate(COUNTRIES)}
Faker.seed(42)


# ─────────────────────────────────────────
# GENERATORS
# ─────────────────────────────────────────

def generate_products(n=120):
    products = []
    pid = 1
    for category, items in CATEGORIES.items():
        lo, hi = PRICE_RANGES[category]
        for item in items:
            for variant in range(1, (n // 30) + 2):
                brand = random.choice(BRANDS)
                price = round(random.uniform(lo, hi), 2)
                discount = round(random.uniform(0, 25), 1)
                stock = random.randint(0, 500)
                rating = round(random.uniform(2.5, 5.0), 1)
                reviews = random.randint(10, 800)

                if random.random() < 0.04:
                    stock = None
                if random.random() < 0.03:
                    rating = None

                products.append({
                    "id": pid,
                    "title": f"{brand} {item} v{variant}",
                    "category": category,
                    "brand": brand,
                    "price": price,
                    "discountPercentage": discount,
                    "stock": stock,
                    "rating": rating,
                    "reviews": reviews,
                    "sku": f"SR-{category[:3].upper()}-{pid:04d}",
                })
                pid += 1
                if pid > n + 1:
                    break
            if pid > n + 1:
                break

    for _ in range(3):
        dup = random.choice(products[:20]).copy()
        dup["id"] = pid
        products.append(dup)
        pid += 1

    return products[:n]


def generate_users(n=100):
    users = []
    all_countries = COUNTRIES * (n // len(COUNTRIES) + 1)
    random.shuffle(all_countries)
    countries_assigned = all_countries[:n]

    for i in range(n):
        country = countries_assigned[i]
        fake = fakers[country]
        city = random.choice(COUNTRY_CITIES[country])
        age = random.randint(22, 55)

        email = fake.email() if random.random() > 0.03 else None

        users.append({
            "id": i + 1,
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "email": email,
            "age": age,
            "country": country,
            "city": city,
            "phone": fake.phone_number(),
            "address": fake.street_address(),
            "retailerType": random.choice(["Department Store", "Sports Chain", "Independent", "Online Retailer", "Superstore"]),
        })

    return users


def generate_carts(users, products, n=200):
    carts = []
    for cid in range(1, n + 1):
        user = random.choice(users)
        n_products = random.randint(1, 6)
        selected = random.sample(products, min(n_products, len(products)))

        cart_products = []
        for p in selected:
            qty = random.randint(5, 120)
            if random.random() < 0.02:
                qty = None
            cart_products.append({
                "id": p["id"],
                "title": p["title"],
                "price": p["price"],
                "quantity": qty,
                "category": p["category"],
                "discountPercentage": p["discountPercentage"],
            })

        order_date = f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        status = random.choices(
            ["confirmed", "shipped", "delivered", "cancelled"],
            weights=[20, 25, 45, 10]
        )[0]

        carts.append({
            "id": cid,
            "userId": user["id"],
            "totalProducts": len(cart_products),
            "products": cart_products,
            "orderDate": order_date,
            "status": status,
            "channel": random.choice(["Direct Sales", "Distributor", "E-commerce B2B"]),
        })

    return carts


# ─────────────────────────────────────────
# BUILD & SAVE
# ─────────────────────────────────────────

def build_all():
    print("Generating products...")
    products = generate_products(120)

    print("Generating users...")
    users = generate_users(100)

    print("Generating carts/orders...")
    carts = generate_carts(users, products, 200)

    data = {
        "products": {
            "products": products,
            "total": len(products),
            "skip": 0,
            "limit": len(products),
        },
        "users": {
            "users": users,
            "total": len(users),
            "skip": 0,
            "limit": len(users),
        },
        "carts": {
            "carts": carts,
            "total": len(carts),
            "skip": 0,
            "limit": len(carts),
        },
    }

    # Ruta relativa al script
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    for key, val in data.items():
        file_path = output_dir / f"{key}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(val, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {file_path} — {val['total']} records")

    return data


if __name__ == "__main__":
    build_all()
    print("\nDone. JSONs ready.")