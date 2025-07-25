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
    You are a local restaurant expert. You will be given a destination.
    Search for top restaurants, local cuisine, and dining experiences in the given destination.
    Focus on: popular restaurants, local specialties, different price ranges, unique dining experiences.
    Output only restaurant options with cuisine types and highlights.
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
    You are a local activities expert. You will be given a destination.
    Search for activities and attractions in the given destination.
    Focus on: tourist attractions, outdoor activities, cultural experiences, entertainment options.
    Output only activity options with brief descriptions.
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
    description="An agent that looks up weather for a given city",
    instruction="Look up weather forecast for the given city.",
    tools=[get_weather],
    output_key="weather_forecast"
)

# Main parallel agent that runs all search agents simultaneously
travel_research_agent = ParallelAgent(
    name="travel_research_agent",
    description="A comprehensive system that simultaneously searches for weather, restaurants, and activities for trip planning",
    sub_agents=[weather_agent, restaurant_search_agent, activities_search_agent],
)

merger_agent = LlmAgent(
     name="merger_agent",
     model=GEMINI_2_5_FLASH_MODEL,
     instruction="""Create a comprehensive travel guide using the provided information:

    Restaurants: {restaurant_options}
    Activities: {activity_options} 
    Weather: {weather_forecast}

    Format:
    ## Travel Guide
    ### Weather Overview
    [Weather summary and planning implications]

    ### Recommended Restaurants
    [List restaurants with cuisine types and highlights]

    ### Things to Do
    [List activities and attractions]

    ### Daily Planning Suggestions
    [2-3 activity-dining combinations considering weather]
    [What to wear and pack based on weather]

    Keep it practical and focused on the provided information only.
    """,
    description="Creates a structured travel guide by combining information about local restaurants, activities, and weather forecasts.",
)

travel_planner_pipeline = SequentialAgent(
    name="travel_planner_pipeline",
    description="A pipeline that creates a travel guide by combining information about local restaurants, activities, and weather forecasts.",
    sub_agents=[travel_research_agent, merger_agent]
)

root_agent = LlmAgent(
    name="root_agent",
    model=GEMINI_2_0_FLASH_MODEL,
    description="You are a travel planner assistant. You will collect travel details and create a comprehensive travel guide.",
    instruction="""You are a travel planner assistant. Collect essential information before creating a travel guide.

    Ask for:
    1. Destination (city/location)
    2. Number of days to stay

    If user provides both in initial message, proceed directly. Otherwise, ask for missing information.

    Example:
    User: "Plan a trip to Tokyo"
    Assistant: "I'd be happy to help plan your trip to Tokyo. How many days are you planning to stay?"

    User: "I want to visit Paris for 5 days"
    Assistant: [Proceed with travel guide creation]

    Once you have all required information, create a comprehensive travel guide.
    """,
    sub_agents=[travel_planner_pipeline]
)