from google.adk.agents import ParallelAgent, LlmAgent, SequentialAgent

from google.adk.tools import google_search
from google.adk import Agent
import requests

GEMINI_2_0_FLASH_MODEL = "gemini-2.0-flash"
GEMINI_2_5_FLASH_MODEL = "gemini-2.5-flash"

# Restaurant Search Agent - Finds dining options
restaurant_search_agent = Agent(
    name="restaurant_search_agent",
    model=GEMINI_2_0_FLASH_MODEL,
    tools=[google_search],
    description="An agent that searches for restaurants and dining experiences in a given destination",
    instruction="""
    You are a food and dining expert. You will be given a destination and you will search for:
    - Top-rated restaurants and cafes
    - Local cuisine specialties
    - Different dining price ranges
    - Unique dining experiences
    Provide a summary of the best dining options with cuisine types and highlights.
    Only research for restaurants and nothing else.

    Output should only contain the restaurant options, no other text.
    """,
    output_key="restaurant_options",
)

# Activities Search Agent - Finds things to do
activities_search_agent = Agent(
    name="activities_search_agent",
    model=GEMINI_2_0_FLASH_MODEL,
    tools=[google_search],
    description="An agent that searches for activities and attractions in a given destination",
    instruction="""
    You are a local activities expert. You will be given a destination and you will search for:
    - Popular tourist attractions
    - Outdoor activities and adventures
    - Cultural experiences and museums
    - Entertainment and nightlife options
    Provide a summary of the best activities with brief descriptions and recommendations.
    Only research for activities and nothing else.

    Output should only contain the activity options, no other text.
    """,
    output_key="activity_options",
)

def get_weather(city: str) -> dict:
    loc = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1}
    ).json()["results"][0]
    lat, lon = loc["latitude"], loc["longitude"]
    w = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat, "longitude": lon,
            "daily": "temperature_2m_max,precipitation_probability_mean",
            "forecast_days": 3, "timezone": "auto"
        }).json()["daily"]
    out = []
    for i, day in enumerate(w["time"]):
        out.append(
            f"{day}: high {w['temperature_2m_max'][i]}°C, "
            f"rain {w['precipitation_probability_mean'][i]}%")
    return "\n".join(out)


weather_agent = Agent(
    name="weather_agent",
    model=GEMINI_2_0_FLASH_MODEL,
    description="Lookup weather in a given city",
    instruction=(
        "You are an assistant specialized in looking up weather for a given city"
    ),
    tools=[get_weather],
    output_key="weather_forecast"
)

# Main parallel agent that runs all search agents simultaneously
information_gathering_agent = ParallelAgent(
    name="information_gathering_agent",
    description="A comprehensive system that simultaneously searches for hotels, restaurants, and activities for trip planning",
    sub_agents=[restaurant_search_agent, activities_search_agent, weather_agent],
)

merger_agent = LlmAgent(
     name="merger_agent",
     model=GEMINI_2_5_FLASH_MODEL,  # Or potentially a more powerful model if needed for synthesis
     instruction="""You are an AI Assistant responsible for creating a comprehensive travel guide based on gathered information.

Your task is to synthesize the research about restaurants, activities, and weather for a given city into a well-structured travel guide. Use only the information provided in the input summaries below.

**Input Summaries:**

*   **Restaurants:**
    {restaurant_options}

*   **Activities:**
    {activity_options} 

*   **Weather Forecast:**
    {weather_forecast}

**Output Format:**

## Travel Guide

### Weather Overview
[Summarize the weather forecast and what it means for planning activities]

### Recommended Restaurants
[List and describe the recommended restaurants, including any notable features, cuisine types, or special recommendations]

### Things to Do
[Organize and describe the suggested activities, attractions, and entertainment options]

### Daily Planning Suggestions
[Provide 2-3 suggestions for how to combine the activities and dining options, taking weather into consideration]

Keep the guide practical and focused on helping travelers make the most of their visit. Only include information that was provided in the input summaries.
""",
     description="Creates a structured travel guide by combining information about local restaurants, activities, and weather forecasts.",
)

itinerary_pipeline = SequentialAgent(
    name="itinerary_pipeline",
    description="A pipeline that creates a travel guide by combining information about local restaurants, activities, and weather forecasts.",
    sub_agents=[information_gathering_agent, merger_agent]
)

root_agent = LlmAgent(
    name="root_agent",
    model=GEMINI_2_0_FLASH_MODEL,
    description="You are a travel planner assistant. You will be given a destination and you will create a travel guide for that destination.",
    instruction="""You are a travel planner assistant. You will be given a destination and you will create a travel guide for that destination.
    """,
    sub_agents=[itinerary_pipeline]
)