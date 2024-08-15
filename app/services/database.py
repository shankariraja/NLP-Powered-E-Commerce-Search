import sqlite3
import json
from app.models.product import Product

def get_db_connection():
    conn = sqlite3.connect('walmart_products.db')
    conn.row_factory = sqlite3.Row
    return conn

def search_products(suggestions):
    conn = get_db_connection()
    c = conn.cursor()

    query, params = build_search_query(suggestions)

    c.execute(query, params)
    results = c.fetchall()

    products = [Product(
        id=row['id'],
        product_name=row['product_name'],
        category_name=row['category_name'],
        final_price=row['final_price'],
        brand=row['brand'],
        rating=row['rating'],
        review_count=row['review_count']
    ).to_dict() for row in results]

    conn.close()
    return products

def build_search_query(suggestions):
    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if suggestions['products']:
        categories = list(set(product['category'] for product in suggestions['products']))
        query += " AND (category_name IN ({}) OR root_category_name IN ({}))".format(
            ','.join('?' * len(categories)),
            ','.join('?' * len(categories))
        )
        params.extend(categories * 2)

    if suggestions['price_range']:
        query += " AND final_price BETWEEN ? AND ?"
        params.extend([suggestions['price_range']['min'], suggestions['price_range']['max']])

    if suggestions['brand']:
        query += " AND brand LIKE ?"
        params.append(f"%{suggestions['brand']}%")

    if suggestions['color']:
        query += " AND colors LIKE ?"
        params.append(f"%{suggestions['color']}%")

    if suggestions['min_rating']:
        query += " AND rating >= ?"
        params.append(suggestions['min_rating'])

    if suggestions['aisle']:
        query += " AND aisle LIKE ?"
        params.append(f"%{suggestions['aisle']}%")

    if suggestions['free_returns'] is not None:
        query += " AND free_returns = ?"
        params.append(1 if suggestions['free_returns'] else 0)

    # Add conditions for keywords
    if suggestions['keywords']:
        keyword_conditions = []
        for keyword in suggestions['keywords']:
            keyword_conditions.append("(product_name LIKE ? OR description LIKE ?)")
            params.extend([f"%{keyword}%", f"%{keyword}%"])
        query += " AND (" + " OR ".join(keyword_conditions) + ")"

    query += " ORDER BY rating DESC, review_count DESC LIMIT 20"

    return query, params