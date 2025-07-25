from google.adk.agents import LlmAgent
import requests

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
    

root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.0-flash",
    description="An agent that can lookup the weather for a given city.",
    instruction="""You are a smart assistant that can lookup the weather for a given city. 
    
    If the user asks for the weather for a city, use the get_weather tool to get the weather for that city.
    If the user has no provided a city, ask them for a city.

    If the user is deviating from the topic, politely remind them that you are a weather assistant and ask them to ask about the weather.
    """,
    tools=[get_weather],
)