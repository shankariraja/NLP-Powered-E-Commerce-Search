# Search AI 
This project implements an AI-powered search system for e-commerce platform using the Gemini language model.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up the database: `python scripts/init_db.py`
6. Set your Gemini API key as an environment variable: `export GEMINI_API_KEY=your_api_key_here`
7. python `app/scripts/init_db.py`
7. Run the application: `python run.py`

## Usage

Send a POST request to `/search` with a JSON body containing the `query` field:

```json
{
  "query": "I need a birthday gift for a 5-year-old boy who likes dinosaurs"
}