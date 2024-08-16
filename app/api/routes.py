from flask import Blueprint, request, jsonify
from app.services.gemini_api import get_gemini_suggestions
from app.services.database import search_products_in_db

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['POST'])
def search():
    try:
        # Check if JSON data is present and valid
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()

        # Check if 'query' is in the request data
        if 'query' not in data:
            return jsonify({"error": "Query parameter is missing"}), 400
        
        query = data['query']

        # Call the function to get suggestions from Gemini API
        suggestions = get_gemini_suggestions(query)
        
        # Check if suggestions are None or not properly formatted
        if not suggestions or not isinstance(suggestions, list):
            return jsonify({"error": "Unable to process query or no valid suggestions found"}), 400
        
        all_products = []

        # Loop through each suggestion and search in the database
        for suggestion in suggestions:
            products = search_products_in_db(suggestion)
            all_products.extend(products)
        
        # Return all matching products
        return jsonify(all_products)
    
    except Exception as e:
        # Catch any unexpected exceptions and return a generic error message
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
