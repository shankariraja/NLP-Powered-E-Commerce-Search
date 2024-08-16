from flask import Blueprint, request, jsonify
from app.services.gemini_api import get_gemini_suggestions
from app.services.database import search_products_in_db

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['POST'])
def search():
    try:
        # Check if JSON data is present and valid
        if not request.is_json:
            print("Debug: Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        print(f"Debug: Received data - {data}")

        # Check if 'query' is in the request data
        if 'query' not in data:
            print("Debug: 'query' parameter is missing")
            return jsonify({"error": "Query parameter is missing"}), 400
        
        query = data['query']
        print(f"Debug: Query parameter - {query}")

        # Call the function to get suggestions from Gemini API
        suggestions = get_gemini_suggestions(query)
        print(f"Debug: Gemini API suggestions - {suggestions}")
        
        # Check if suggestions are None or not properly formatted
        if not suggestions or not isinstance(suggestions, list):
            print("Debug: No valid suggestions found or suggestions not formatted as a list")
            return jsonify({"error": "Unable to process query or no valid suggestions found"}), 400
        
        all_products = []

        # Loop through each suggestion and search in the database
        for suggestion in suggestions:
            print(f"Debug: Processing suggestion - {suggestion}")
            products = search_products_in_db(suggestion)
            all_products.extend(products)
            print(f"Debug: Found products - {products}")
        
        # Return all matching products
        print(f"Debug: All matching products - {all_products}")
        return jsonify(all_products)
    
    except Exception as e:
        print(f"Detailed error: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
