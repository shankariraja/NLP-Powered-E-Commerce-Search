import sqlite3
from app.models.product import Product

def search_products_in_db(suggestion):
    conn = sqlite3.connect('walmart_products.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Generalize the query for product types and categories
    product_type_query = " OR ".join([
        "product_name LIKE ?",
        "product_name LIKE ?"
    ])
    
    category_query = " OR ".join([
        "category_name LIKE ?",
        "category_name LIKE ?"
    ])

    # Prepare the keywords query
    keywords_query = " OR ".join([
        "product_name LIKE ?",
        "description LIKE ?"
    ])

    # Construct the SQL query
    query = f"""
    SELECT * FROM products
    WHERE ({product_type_query}) AND ({category_query})
    """
    
    # Initialize query parameters
    params = [
        f"%{suggestion['product_type']}%",
        f"%{suggestion['product_type']}%",  # For synonyms or variations
        f"%{suggestion['category']}%",
        f"%{suggestion['category']}%"  # For broader category matches
    ]

    # Append keywords to query and parameters
    if suggestion.get('keywords'):
        query += f" AND ({keywords_query})"
        for keyword in suggestion['keywords']:
            params.extend([f"%{keyword}%", f"%{keyword}%"])

    # Optionally add additional filters based on provided suggestion
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

    cursor.execute(query, params)
    results = cursor.fetchall()

    # Map results to Product instances and convert to dictionaries
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
