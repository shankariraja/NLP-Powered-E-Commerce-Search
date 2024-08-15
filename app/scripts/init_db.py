import sqlite3
import csv
import json
import os
from ..config.config import DATABASE_PATH

def init_db():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Create table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY,
                  timestamp TEXT,
                  url TEXT,
                  final_price REAL,
                  sku TEXT,
                  currency TEXT,
                  gtin TEXT,
                  specifications TEXT,
                  image_urls TEXT,
                  top_reviews TEXT,
                  rating_stars REAL,
                  related_pages TEXT,
                  available_for_delivery INTEGER,
                  available_for_pickup INTEGER,
                  brand TEXT,
                  breadcrumbs TEXT,
                  category_ids TEXT,
                  review_count INTEGER,
                  description TEXT,
                  product_id TEXT,
                  product_name TEXT,
                  review_tags TEXT,
                  category_url TEXT,
                  category_name TEXT,
                  category_path TEXT,
                  root_category_url TEXT,
                  root_category_name TEXT,
                  upc TEXT,
                  tags TEXT,
                  main_image TEXT,
                  rating REAL,
                  unit_price REAL,
                  unit TEXT,
                  aisle TEXT,
                  free_returns INTEGER,
                  sizes TEXT,
                  colors TEXT,
                  seller TEXT,
                  other_attributes TEXT,
                  customer_reviews TEXT,
                  ingredients TEXT,
                  initial_price REAL,
                  discount REAL,
                  ingredients_full TEXT,
                  categories TEXT)''')
    conn.commit()
    conn.close()

def convert_to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def insert_data_from_csv(filename):
    # Construct the full path to the CSV file
    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, '../data', filename)

    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            # Convert some fields to appropriate types
            row['final_price'] = convert_to_float(row['final_price'])
            row['rating_stars'] = convert_to_float(row['rating_stars'])
            row['available_for_delivery'] = 1 if row['available_for_delivery'].lower() == 'true' else 0
            row['available_for_pickup'] = 1 if row['available_for_pickup'].lower() == 'true' else 0
            row['review_count'] = int(row['review_count']) if row['review_count'] else None
            row['rating'] = convert_to_float(row['rating'])
            row['unit_price'] = convert_to_float(row['unit_price'])
            row['free_returns'] = 1 if row['free_returns'].lower() == 'true' else 0
            row['initial_price'] = convert_to_float(row['initial_price'])
            row['discount'] = convert_to_float(row['discount'])

            # Convert list-like strings to JSON
            list_fields = ['image_urls', 'top_reviews', 'related_pages', 'breadcrumbs', 'category_ids', 'review_tags', 'tags', 'sizes', 'colors', 'customer_reviews', 'categories']
            for field in list_fields:
                if row[field]:
                    try:
                        row[field] = json.dumps(eval(row[field]))
                    except:
                        row[field] = json.dumps([row[field]])

            # Convert dict-like strings to JSON
            dict_fields = ['specifications', 'other_attributes']
            for field in dict_fields:
                if row[field]:
                    try:
                        row[field] = json.dumps(eval(row[field]))
                    except:
                        row[field] = json.dumps({})

            c.execute('''INSERT INTO products 
                         (timestamp, url, final_price, sku, currency, gtin, specifications, image_urls, top_reviews, 
                          rating_stars, related_pages, available_for_delivery, available_for_pickup, brand, breadcrumbs, 
                          category_ids, review_count, description, product_id, product_name, review_tags, category_url, 
                          category_name, category_path, root_category_url, root_category_name, upc, tags, main_image, 
                          rating, unit_price, unit, aisle, free_returns, sizes, colors, seller, other_attributes, 
                          customer_reviews, ingredients, initial_price, discount, ingredients_full, categories)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                 ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                      tuple(row.values()))

    conn.commit()
    conn.close()

# Run these functions to set up the database and insert data
init_db()
insert_data_from_csv('walmart_product.csv')
