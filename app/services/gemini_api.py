import requests
import json
import re
from ..config.config import GEMINI_API_KEY, GEMINI_API_URL
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_suggestions(query):
    system_prompt = """
        You are an AI assistant for Walmart's e-commerce platform. Analyze the user's query and provide a product suggestion in the following format:

        Product Type: [General type of product]
        Category: [Broad category of the product]
        Price Range: [Minimum price] - [Maximum price] (Only if specified in query)
        Brand: [Brand name] (Only if specified in query)
        Color: [Color] (Only if specified in query)
        Min Rating: [Minimum rating] (Only if specified in query)
        Keywords: [Comma-separated list of relevant keywords]
        Aisle: [General aisle or department]
        Free Returns: [Yes/No/Any] (Only if specified in query)

        Provide 25 product suggestions only in the mentioned format, the best match product will come first followed by others like a rank-based search result. Use 'Any' for fields that are not applicable. Include Price Range, Brand, Color, and Min Rating only if they are explicitly mentioned in the user's query. Use general terms for Product Type, Category, and Aisle.
    """

    prompt = f"{system_prompt}\n\nUser query: {query}"

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                stop_sequences=["User query:"],
                max_output_tokens=10000,
                temperature=0.2,
            ),
        )
    except Exception as e:
        print(f"Error generating content from Gemini API: {e}")
        return None

    content = parse_gemini_response(response)
    if content is not None:
        return post_process_gemini_suggestions(content)
    
    print("Failed to get a complete response.")
    return None

def parse_gemini_response(response):
    try:
        if hasattr(response, 'text'):
            response_text = response.text
        else:
            response_text = str(response)

        # Return the raw text for post-processing
        return response_text

    except Exception as e:
        print(f"Unexpected error during response parsing: {e}")
        return None

def post_process_gemini_suggestions(raw_suggestions):
    # Debugging statement to verify the raw suggestions input
    print(f"Debug: Raw suggestions input - {raw_suggestions}")

    # Split the raw response into individual product suggestions based on a consistent marker
    suggestions = raw_suggestions.split("**")
    
    # Debugging statement to verify the split suggestions
    print(f"Debug: Split suggestions - {suggestions}")

    processed_suggestions = []
    
    for suggestion in suggestions:
        # Strip unnecessary whitespace
        suggestion = suggestion.strip()
        if not suggestion:
            continue

        # Debugging statement to verify each stripped suggestion
        print(f"Debug: Processing suggestion - {suggestion}")

        # Split the suggestion into lines and initialize a dictionary to hold processed data
        lines = suggestion.split("\n")
        product_data = {}

        for line in lines:
            if ':' in line:
                try:
                    # Extract key-value pairs
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_')
                    value = value.strip()

                    # Debugging statement to verify each key-value pair
                    print(f"Debug: Extracted key-value pair - {key}: {value}")
                    
                    # Handle specific keys differently based on their format
                    if key == 'keywords':
                        product_data[key] = [k.strip() for k in value.split(',')]
                    elif key == 'price_range':
                        min_price, max_price = value.split('-')
                        product_data[key] = {
                            'min': float(min_price.strip().replace('$', '').replace(',', '')),
                            'max': float(max_price.strip().replace('$', '').replace(',', ''))
                        }
                    elif key == 'min_rating':
                        product_data[key] = float(value) if value.lower() != 'any' else None
                    else:
                        product_data[key] = value if value.lower() != 'any' else None

                    # Debugging statement to verify the processed product data after each key-value pair
                    print(f"Debug: Updated product data - {product_data}")
                except ValueError as ve:
                    print(f"Error processing line '{line}': {ve}")
                    continue
        
        # Append the processed product data to the list
        if product_data:
            processed_suggestions.append(product_data)
            # Debugging statement to verify the addition of processed product data to the list
            print(f"Debug: Added processed product data to the list - {product_data}")
    
    # Debugging statement to verify the final processed suggestions
    print(f"Debug: Final processed suggestions - {processed_suggestions}")

    return processed_suggestions

