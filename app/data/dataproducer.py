import csv
from datetime import datetime, timedelta
import random
import json
import os
import sqlite3

# Function to generate random timestamps
def random_timestamp(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# Define the start and end date for random timestamp generation
start_date = datetime(2024, 8, 1)
end_date = datetime(2024, 8, 16)

# Define the expanded list of sample data for various attributes
brands = [
    "BabyBrand", "GiftMakers", "CookMaster", "SpiceHouse", "ToysWorld", "ComfortSleep", "FlavorTown", 
    "HappyBaby", "PartyGifts", "GourmetChefs", "HerbEssence", "PlayLand", "SnugDream", "DeliciousDishes",
    "JoyfulGifts", "LittleWonders", "HomeComfort", "TasteOfIndia", "PlayfulKidz", "PureSpice", 
    "CuddleCare", "TasteBuds", "CozyNest", "OrganicSpices", "TenderTouch", "FestiveGifts", 
    "GourmetTreats", "BabyJoy", "FreshFlavors", "UltimateComfort", "SpiceKing", "BabyEssentials",
    "GourmetGalore", "NurseryNeeds", "SpiceIsland", "BeddingBoutique", "ToysParadise", "ComfortCradle"
]

categories = [
    "Baby Gifts", "Birthday Gifts", "Boy Baby Gifts", "Cooking Ingredients", "Spices", "Bedding", 
    "Toys", "Feeding", "Toddler Toys", "Baby Clothing", "Kitchen Essentials", "Party Supplies", 
    "Nursery Decor", "Herbs & Spices", "Baby Care", "Organic Foods", "Baby Furniture", "Playground Equipment", 
    "Children's Books", "Bathing Essentials", "Infant Safety", "Newborn Care", "Parenting Guides", 
    "Baby Health", "Kitchen Gadgets", "Cuddly Toys", "Learning Toys", "Eco-friendly Products", 
    "Organic Bedding", "Traditional Spices", "Exotic Ingredients", "Cooking Utensils"
]

colors = [
    "Red", "Blue", "Pink", "Green", "Yellow", "Brown", "White", "Purple", "Orange", "Black", "Gray", 
    "Aqua", "Lavender", "Teal", "Navy", "Beige", "Coral", "Mint", "Silver", "Gold", "Ivory", "Peach", 
    "Maroon", "Olive", "Turquoise", "Magenta", "Burgundy", "Cyan", "Bronze", "Cream"
]

sizes = [
    "Small", "Medium", "Large", "100g", "250g", "500g", "1kg", "2kg", "50ml", "100ml", "200ml", "1L", 
    "2L", "3L", "Tiny", "Mini", "XXL", "Jumbo", "Extra Small", "Extra Large", "Family Pack", "Single", 
    "Economy Pack", "Regular", "Travel Size", "Bulk Pack", "Standard", "Portable", "Compact"
]

aisles = [
    "Gifts", "Cooking", "Spices", "Toys", "Bedding", "Feeding", "Clothing", "Books", "Home Decor", 
    "Safety", "Furniture", "Health", "Essentials", "Outdoor Play", "Bathing", "Party Supplies", 
    "Organic", "Kitchen Tools", "Nursery", "Groceries", "Baby Gear", "Kids Clothing", "Eco-friendly", 
    "Gourmet Food", "Home & Kitchen", "Toys & Games", "Bath & Body", "Diapering", "Car Seats", "Travel Gear"
]

sellers = [
    "SellerA", "SellerB", "SellerC", "SellerD", "SellerE", "SellerF", "SellerG", "SellerH", 
    "SellerI", "SellerJ", "SellerK", "SellerL", "SellerM", "SellerN", "SellerO", "SellerP", 
    "SellerQ", "SellerR", "SellerS", "SellerT", "SellerU", "SellerV", "SellerW", "SellerX", 
    "SellerY", "SellerZ", "SellerAA", "SellerBB", "SellerCC", "SellerDD", "SellerEE"
]

# Function to generate random product data
def generate_product_data(index):
    product = {
        "timestamp": random_timestamp(start_date, end_date).isoformat() + "Z",
        "url": f"https://example.com/product{index}",
        "final_price": round(random.uniform(5.0, 100.0), 2),
        "sku": f"SKU{str(index).zfill(3)}",
        "currency": "USD",
        "gtin": "".join([str(random.randint(0, 9)) for _ in range(13)]),
        "specifications": json.dumps({
            "Weight": random.choice(sizes),
            "Color": random.choice(colors)
        }),
        "image_urls": json.dumps([f"https://example.com/images/product{index}-1.jpg"]),
        "top_reviews": json.dumps([f"Review for product {index}. High quality and well-made."]),
        "rating_stars": round(random.uniform(3.0, 5.0), 1),
        "related_pages": json.dumps([f"https://example.com/related/product{index}"]),
        "available_for_delivery": 1 if random.choice(["Yes", "No"]) == "Yes" else 0,
        "available_for_pickup": 1 if random.choice(["Yes", "No"]) == "Yes" else 0,
        "brand": random.choice(brands),
        "breadcrumbs": json.dumps([f"Home > {random.choice(categories)}"]),
        "category_ids": json.dumps([f"{index % 1000}"]),
        "review_count": random.randint(1, 100),
        "description": f"Description for product {index}",
        "product_id": f"PID{str(index).zfill(4)}",
        "product_name": f"Product {index} Name",
        "review_tags": json.dumps([f"tag{index}", "category", "popular"]),
        "category_url": f"https://example.com/categories/{categories[index % len(categories)].replace(' ', '-').lower()}",
        "category_name": categories[index % len(categories)],
        "category_path": f"Grocery & Gourmet Food > {categories[index % len(categories)]}",
        "root_category_url": "https://example.com/categories",
        "root_category_name": "Grocery & Gourmet Food",
        "upc": "".join([str(random.randint(0, 9)) for _ in range(12)]),
        "tags": json.dumps([f"tag{index}", "product", "category"]),
        "main_image": f"https://example.com/images/product{index}-main.jpg",
        "rating": round(random.uniform(3.0, 5.0), 1),
        "unit_price": round(random.uniform(1.0, 20.0), 2),
        "unit": random.choice(sizes),
        "aisle": random.choice(aisles),
        "free_returns": 1 if random.choice(["Yes", "No"]) == "Yes" else 0,
        "sizes": json.dumps([random.choice(sizes)]),
        "colors": json.dumps([random.choice(colors)]),
        "seller": random.choice(sellers),
        "other_attributes": json.dumps({f"attribute{index}": "value"}),
        "customer_reviews": json.dumps([f"Customer review {index}: Satisfied with the quality."]),
        "ingredients": f"Ingredients for product {index}",
        "initial_price": round(random.uniform(10.0, 150.0), 2),
        "discount": round(random.uniform(5.0, 30.0), 2),
        "ingredients_full": json.dumps({"Ingredient": f"Full list for product {index}"}),
        "categories": json.dumps([categories[index % len(categories)]])
    }
    return product

# Generate the data
data = [generate_product_data(i) for i in range(1, 501)]

# Write the data to a CSV file
csv_columns = data[0].keys()
csv_file = "walmart_product.csv"
try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(data)
except IOError:
    print("I/O error")
