import requests
import json
from ..config.config import GEMINI_API_KEY, GEMINI_API_URL
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key='AIzaSyD-LRxvIZOgmArqcJwXE3rpixFk5-LoHJE')


def get_gemini_suggestions(query, max_retries=3):
    model = genai.GenerativeModel("gemini-1.5-flash")

    system_prompt = """
    You are an AI assistant for Walmart's e-commerce platform. Analyze the user's query and provide product suggestions.
    Output should be a JSON string with the following structure:
    {
        "products": [
            {"name": "Product Name", "category": "Category"},
            ...
        ],
        "price_range": {"min": 0, "max": 100},
        "brand": "Preferred Brand",
        "color": "Preferred Color",
        "min_rating": 4.0,
        "keywords": ["relevant", "search", "terms"],
        "aisle": "Relevant Aisle",
        "free_returns": true/false
    }
    Provide only one product suggestions. If any field is not applicable, use null.
    """
    
    prompt = f"{system_prompt}\n\nUser query: {query}"

    for attempt in range(max_retries):
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                stop_sequences=["x"],
                max_output_tokens=512,  # Adjusted token limit
                temperature=1.0,
            ),
        )

        content = parse_gemini_response(response)
        if content is not None:
            return content
        print(f"Retrying... ({attempt + 1}/{max_retries})")

    print("Failed to get a complete response after retries.")
    return None

def parse_gemini_response(response):
    try:
        if hasattr(response, 'text'):
            response_text = response.text
        else:
            response_text = str(response)

        # Log the raw response for debugging
        print("Raw response:", response_text)

        # Close incomplete JSON
        if response_text.count('{') > response_text.count('}'):
            response_text += '}' * (response_text.count('{') - response_text.count('}'))
        if response_text.count('[') > response_text.count(']'):
            response_text += ']' * (response_text.count('[') - response_text.count(']'))
        
        try:
            content = json.loads(response_text)
            return content
        except json.JSONDecodeError as e:
            print(f"Error parsing Gemini response: {e}")
            return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Example usage
query = "Looking for a baby toy."
suggestions = get_gemini_suggestions(query)
print(suggestions)
