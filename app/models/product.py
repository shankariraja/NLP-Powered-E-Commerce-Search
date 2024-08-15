class Product:
    def __init__(self, id, product_name, category_name, final_price, brand, rating, review_count):
        self.id = id
        self.product_name = product_name
        self.category_name = category_name
        self.final_price = final_price
        self.brand = brand
        self.rating = rating
        self.review_count = review_count

    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'category_name': self.category_name,
            'final_price': self.final_price,
            'brand': self.brand,
            'rating': self.rating,
            'review_count': self.review_count
        }