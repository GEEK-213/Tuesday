"""Tuesday — Web Search Tool. Queries DuckDuckGo and returns structured results."""

import json
from ddgs import DDGS


def search_web(query: str) -> str:
    """Search DuckDuckGo for the query and return top 3 results as JSON."""
    try:
        results = DDGS().text(query, max_results=3)

        # Build a clean list of title/link/snippet dicts
        formatted = [
            {
                "title": r.get("title", ""),
                "link": r.get("href", ""),
                "snippet": r.get("body", ""),
            }
            for r in results
        ]

        return json.dumps({"status": "success", "results": formatted}, indent=2)

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


if __name__ == "__main__":
    print("🔍 Tuesday Web Search")
    print("=" * 40)
    print(search_web("latest Python news"))
