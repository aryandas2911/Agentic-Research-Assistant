from dotenv import load_dotenv
import os
from serpapi import GoogleSearch

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not SERPAPI_API_KEY:
    raise ValueError("SERPAPI_API_KEY not found in .env")

def search_web(query:str):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    organic_results = results.get("organic_results", [])

    formatted_results = []

    for result in organic_results:
        formatted_results.append({
            "title": result.get("title"),
            "url": result.get("link"),
            "snippet": result.get("snippet"),
        })

    return formatted_results

if __name__ == "__main__":
    results = search_web("latest developments in AI agents")
    print(results)