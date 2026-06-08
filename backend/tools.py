import requests

from langchain_core.tools import tool
from langchain_community.tools import (
    DuckDuckGoSearchRun
)

from backend.config import (
    ALPHA_VANTAGE_API_KEY,
    OPENWEATHER_API_KEY,
    SERPAPI_API_KEY
)

search_tool = DuckDuckGoSearchRun(
    region="us-en"
)

@tool
def get_stock_price(
    symbol: str
) -> dict:

    """
    Fetch latest stock price.
    """

    url = (
        f"https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE"
        f"&symbol={symbol}"
        f"&apikey={ALPHA_VANTAGE_API_KEY}"
    )

    response = requests.get(url)

    return response.json()

@tool
def get_weather(
    city: str
) -> dict:

    """
    Fetch current weather.
    """

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={OPENWEATHER_API_KEY}"
    )

    try:

        response = requests.get(url)

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }
        
@tool
def find_local_events(
    city: str
) -> dict:

    """
    Find local events.
    """

    try:

        url = (
            f"https://serpapi.com/search.json"
            f"?engine=google_events"
            f"&q=Events in {city}"
            f"&api_key={SERPAPI_API_KEY}"
        )

        response = requests.get(url)

        data = response.json()

        events = []

        for event in data.get(
            "events_results",
            []
        )[:5]:

            events.append(
                {
                    "title":
                        event.get("title"),

                    "date":
                        event.get(
                            "date",
                            {}
                        ).get(
                            "start_date"
                        ),

                    "address":
                        event.get(
                            "address",
                            [""]
                        )[0],

                    "link":
                        event.get("link")
                }
            )

        return {
            "city": city,
            "events": events
        }

    except Exception as e:

        return {
            "error": str(e)
        }