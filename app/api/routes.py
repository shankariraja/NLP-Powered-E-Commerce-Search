from flask import Blueprint, request, jsonify
from app.services.gemini_api import get_gemini_suggestions
from app.services.database import search_products

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    
    suggestions = get_gemini_suggestions(query)
    
    if not suggestions:
        return jsonify({"error": "Unable to process query"}), 400
    
    products = search_products(suggestions)
    
    return jsonify({
        "products": products,
        "suggested_keywords": suggestions['keywords']
    })