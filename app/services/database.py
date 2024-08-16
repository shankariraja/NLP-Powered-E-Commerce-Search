import sqlite3
from app.models.product import Product

def search_products_in_db(suggestion):
    # Debugging statement to verify the formed suggestion
    print(f"Debug: Suggestion criteria - {suggestion}")

    try:
        conn = sqlite3.connect('walmart_products.db')
        print("Debug: Successfully connected to the Walmart database.")
    except sqlite3.Error as e:
        print(f"Debug: Error connecting to the Walmart database - {e}")
        return []

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    # Add filters based on suggestion
    if suggestion.get('product_type'):
        query += " AND (product_name LIKE ? OR category_name LIKE ?)"
        params.extend([f"%{suggestion['product_type']}%", f"%{suggestion['product_type']}%"])

    if suggestion.get('category'):
        query += " AND category_name LIKE ?"
        params.append(f"%{suggestion['category']}%")

    if suggestion.get('keywords'):
        keyword_conditions = " OR ".join(["product_name LIKE ? OR description LIKE ?"] * len(suggestion['keywords']))
        query += f" AND ({keyword_conditions})"
        for keyword in suggestion['keywords']:
            params.extend([f"%{keyword}%", f"%{keyword}%"])

    if suggestion.get('brand'):
        query += " AND brand LIKE ?"
        params.append(f"%{suggestion['brand']}%")

    if suggestion.get('price_range'):
        query += " AND final_price BETWEEN ? AND ?"
        params.extend([suggestion['price_range']['min'], suggestion['price_range']['max']])

    if suggestion.get('color'):
        query += " AND colors LIKE ?"
        params.append(f"%{suggestion['color']}%")

    if suggestion.get('min_rating'):
        query += " AND rating >= ?"
        params.append(float(suggestion['min_rating']))

    query += " ORDER BY rating DESC, review_count DESC LIMIT 10"

    # Debugging statement to verify the formed SQL query
    print(f"Debug: SQL Query - {query}")
    print(f"Debug: SQL Parameters - {params}")

    cursor.execute(query, params)
    results = cursor.fetchall()

    products = [Product(
        id=row['id'],
        product_name=row['product_name'],
        category_name=row['category_name'],
        final_price=row['final_price'],
        brand=row['brand'],
        rating=row['rating'],
        review_count=row['review_count'],
        image_url=row['main_image'],
        description=row['description']
    ).to_dict() for row in results]

    conn.close()
    return products
