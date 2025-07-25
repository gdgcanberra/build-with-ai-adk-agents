# BuildWithAI Workshop- AI Agents with ADK

Welcome to the Build with AI - Hands-On workshop! In this guide, you'll learn how to build agents using the Google Agent Development Kit (ADK) through three progressive examples: a simple Hello World agent, a tool-calling weather agent, and a sophisticated multi-agent travel planner.

---

## Table of Contents
1. [Prerequisites & Environment Setup](#prerequisites--environment-setup)
2. [Agent Definition & Key Fields](#agent-definition--key-fields)
3. [Testing Your Agents](#testing-your-agents)
4. [Step 1: Hello World Agent](#step-1-hello-world-agent)
5. [Step 2: Tool Calling Agent](#step-2-tool-calling-agent)
6. [Step 3: Travel Agent](#step-3-travel-agent)
7. [Running Your Agents](#running-your-agents)
8. [Troubleshooting](#troubleshooting)
9. [Further Resources](#further-resources)

---

## Prerequisites & Environment Setup

### Requirements
- **Python 3.9+** (recommended: 3.10 or 3.11)
- **pip** (Python package manager)
- **A code editor** (VS Code, PyCharm, etc.)
- **Terminal access**
- A [Google AI Studio](https://aistudio.google.com/app/apikey) API key

<details>
<summary><strong>Installing Python and pip (click to expand)</strong></summary>

If you don't already have Python and pip installed, follow these steps:

1. **Check if Python is installed:**
   ```bash
   python --version
   # or
   python3 --version
   ```
   If you see a version number (e.g., `Python 3.10.12`), you're good to go!

2. **Install Python:**
   - Download the latest Python 3.x installer for your OS from the [official Python website](https://www.python.org/downloads/).
   - Follow the installation instructions for your platform:
     - [Windows installation guide](https://docs.python.org/3/using/windows.html)
     - [macOS installation guide](https://docs.python.org/3/using/mac.html)
     - [Linux installation guide](https://docs.python.org/3/using/unix.html)
   - Make sure to check the box to "Add Python to PATH" during installation (on Windows).

3. **Verify pip installation:**
   ```bash
   pip --version
   # or
   pip3 --version
   ```
   If pip is not found, you can [install pip by following the official guide](https://pip.pypa.io/en/stable/installation/).

</details>

### Project Setup
1. **Create the project structure:**
   ```bash
   mkdir adk-agents-build-with-ai
   cd adk-agents-build-with-ai
   ```

2. **Create the agent directories:**
   ```bash
   mkdir hello_world tool_calling_agent travel_agent
   touch hello_world/__init__.py tool_calling_agent/__init__.py travel_agent/__init__.py
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install google-adk requests
   ```

### Authentication Setup
1. **Get your API key:**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and create an API key

2. **Create environment file:**
   Create a `.env` file in your project root with the following content:
   ```
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=YOUR_API_KEY_HERE
   ```
   Replace `YOUR_API_KEY_HERE` with your actual API key.

---

## Agent Definition & Key Fields

Agents in ADK are defined as Python objects with several important fields. Understanding these fields is crucial for building effective and well-behaved agents. For more details, see the [ADK Agent Documentation](https://google.github.io/adk-docs/agents/llm-agents/).

### Key Fields

| Field        | Description |
|--------------|-------------|
| `name`       | A unique identifier for your agent. Used for routing and debugging. Should be short, lowercase, and descriptive (e.g., `root_agent`, `weather_agent`). |
| `model`      | The model your agent uses for reasoning and language generation. For Gemini, use `gemini-2.0-flash` or `gemini-2.5-flash`. See [Models & Authentication](https://google.github.io/adk-docs/agents/models/) for more info. |
| `description`| A concise summary of the agent's capabilities. Used by other agents for routing and by the Dev UI for display. Make it specific (e.g., "Handles weather queries for any city"). |
| `instruction`| The system prompt that defines your agent's behavior. This is where you specify the agent's persona, task boundaries, and how it should respond. See [LLM Agent Instructions](https://google.github.io/adk-docs/agents/llm-agents/#instruction) for best practices. |

#### Example
```python
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.0-flash",
    description="You are a helpful assistant that can answer questions and help with tasks.",
    instruction="""You are a helpful assistant that can answer questions and help with tasks.""",
    tools=[],
)
```

- **name**: `root_agent` — uniquely identifies this agent.
- **model**: `gemini-2.0-flash` — uses the Gemini model for responses.
- **description**: Explains the agent's purpose for routing and UI.
- **instruction**: Sets the agent's persona and boundaries.

For more on agent types and advanced configuration, see:
- [LLM Agents](https://google.github.io/adk-docs/agents/llm-agents/)
- [Workflow Agents (Sequential, Parallel, Loop)](https://google.github.io/adk-docs/agents/workflow-agents/)
- [Multi-Agent Systems](https://google.github.io/adk-docs/agents/multi-agent-systems/)

---

## Testing Your Agents

Once you have defined an agent, you can test it using the ADK CLI. There are two main ways to interact with your agents:

### 1. Run an agent in the terminal
Use the `adk run` command to interact with your agent directly in the terminal:

```bash
adk run <agent_folder>
```
- Example:
  ```bash
  adk run hello_world
  ```
- This will start a prompt where you can type messages and see the agent's responses.

### 2. Use the ADK Dev UI (Web Interface)
The Dev UI provides a graphical interface for chatting with your agents and inspecting their reasoning steps.

```bash
adk web
```
- This will start a local web server (usually at http://localhost:8000).
- Open your browser and select your agent (e.g., `hello_world`, `tool_calling_agent`, or `travel_agent`) from the dropdown.
- You can view function calls, agent reasoning, and more in the Events tab.

For more details, see the [Running Agents documentation](https://google.github.io/adk-docs/running-agents/).

---

## Step 1: Hello World Agent

Let's start with the simplest agent - a basic conversational assistant.

### Implementation
Create `hello_world/agent.py`:

```python
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.0-flash",
    description="You are a helpful assistant that can answer questions and help with tasks.",
    instruction="""You are a helpful assistant that can answer questions and help with tasks.""",
    tools=[],
)
```

### Key Concepts
- **LlmAgent**: The basic agent type for simple conversational AI
- **model**: Specifies which Gemini model to use
- **description**: Used by other agents for routing decisions
- **instruction**: The system prompt that defines the agent's behavior
- **tools**: List of functions the agent can call (empty for this basic example)

### Testing
Run the ADK Dev UI and test with prompts like:
- "Hello, how are you?"
- "What can you help me with?"
- "Tell me a joke"

---

## Step 2: Tool Calling Agent

Now let's build an agent that can call external tools - a weather assistant.

### Implementation
Create `tool_calling_agent/agent.py`:

```python
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
```

### Key Concepts
- **Tool Functions**: Custom functions that agents can call
- **Function Parameters**: Tools can accept parameters (like `city: str`)
- **Return Values**: Tools return data that the agent can use in responses
- **Tool Integration**: The `tools=[get_weather]` parameter makes the function available to the agent

### Weather Tool Breakdown
The `get_weather` function:
1. **Geocoding**: Converts city name to coordinates using Open-Meteo API
2. **Weather Data**: Fetches 3-day forecast with temperature and precipitation
3. **Formatting**: Returns a human-readable weather summary

### Testing
Test with prompts like:
- "What's the weather in Tokyo?"
- "How's the weather in Paris?"
- "Tell me about the weather in New York"

---

## Step 3: Travel Agent

Now let's build a sophisticated multi-agent system that combines parallel processing and sequential workflows. We'll break this down into manageable steps.

### Step 3.1: Set up the foundation
First, create the basic structure and imports in `travel_agent/agent.py`:

```python
from google.adk.agents import ParallelAgent, LlmAgent, SequentialAgent
from google.adk.tools import google_search
from google.adk import Agent
import requests

GEMINI_2_0_FLASH_MODEL = "gemini-2.0-flash"
GEMINI_2_5_FLASH_MODEL = "gemini-2.5-flash"
```

### Step 3.2: Create the weather tool
Add the weather function (same as in Step 2):

```python
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
```

### Step 3.3: Create specialized agents
Add the restaurant search agent:

```python
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
```

Add the activities search agent:

```python
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
```

Add the weather agent:

```python
weather_agent = Agent(
    name="weather_agent",
    model=GEMINI_2_0_FLASH_MODEL,
    description="An agent that looks up weather for a given city",
    instruction="Look up weather forecast for the given city.",
    tools=[get_weather],
    output_key="weather_forecast"
)
```

### Step 3.4: Create the parallel agent
Combine all research agents to run simultaneously:

```python
travel_research_agent = ParallelAgent(
    name="travel_research_agent",
    description="A comprehensive system that simultaneously searches for weather, restaurants, and activities for trip planning",
    sub_agents=[weather_agent, restaurant_search_agent, activities_search_agent],
)
```

### Step 3.5: Create the merger agent
Add the agent that combines all the research results:

```python
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
```

### Step 3.6: Create the pipeline
Connect the research and merger agents in sequence:

```python
travel_planner_pipeline = SequentialAgent(
    name="travel_planner_pipeline",
    description="A pipeline that creates a travel guide by combining information about local restaurants, activities, and weather forecasts.",
    sub_agents=[travel_research_agent, merger_agent]
)
```

### Step 3.7: Create the root agent
Add the final agent that handles user interaction:

```python
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
```

### Key Concepts

#### Agent Types
- **Agent**: Basic agent with tools and output keys
- **ParallelAgent**: Runs multiple agents simultaneously
- **SequentialAgent**: Runs agents in sequence, passing outputs between them
- **LlmAgent**: Conversational agent with optional sub-agents

#### Multi-Agent Architecture
1. **Specialized Agents**: Each agent has a specific role (weather, restaurants, activities)
2. **Parallel Processing**: All research agents run simultaneously for efficiency
3. **Sequential Synthesis**: Results are combined by a merger agent
4. **Root Agent**: Handles user interaction and orchestrates the workflow

#### Output Keys
- `output_key="restaurant_options"`: Names the output for use by other agents
- `{restaurant_options}`: Template variables in merger agent instructions

### Agent Instructions Breakdown

#### Restaurant Search Agent
```
You are a local restaurant expert. You will be given a destination.
Search for top restaurants, local cuisine, and dining experiences in the given destination.
Focus on: popular restaurants, local specialties, different price ranges, unique dining experiences.
Output only restaurant options with cuisine types and highlights.
```

#### Activities Search Agent
```
You are a local activities expert. You will be given a destination.
Search for activities and attractions in the given destination.
Focus on: tourist attractions, outdoor activities, cultural experiences, entertainment options.
Output only activity options with brief descriptions.
```

#### Merger Agent
```
Create a comprehensive travel guide using the provided information:

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
```

#### Root Agent
```
You are a travel planner assistant. Collect essential information before creating a travel guide.

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
```

### Testing
Test with prompts like:
- "Plan a trip to Tokyo"
- "I want to visit Paris for 5 days"
- "What should I do in Rome?"

---

## Running Your Agents

### Launch the ADK Dev UI
1. **Navigate to the project root:**
   ```bash
   cd /path/to/adk-agents-build-with-ai
   ```

2. **Launch the ADK Dev UI:**
   ```bash
   adk web
   ```
   This starts a local web server (usually at http://localhost:8000).

3. **Select your agent:**
   - Choose from the dropdown: `hello_world`, `tool_calling_agent`, or `travel_agent`

### Testing Each Agent

#### Hello World Agent
- Try: "Hello, how are you?"
- Try: "What can you help me with?"

#### Tool Calling Agent
- Try: "What's the weather in Tokyo?"
- Try: "How's the weather in Paris?"

#### Travel Agent
- Try: "Plan a trip to Rome"
- Try: "I want to visit Tokyo for 3 days"

---

## Troubleshooting

### Common Issues
- **Agent not showing in Dev UI?**
  - Make sure you're running `adk web` from the project root
  - Check for typos in agent names
  - Verify `.env` files are in the correct directories

- **Authentication errors?**
  - Double-check your API key in the `.env` files
  - Ensure the API key is valid and has proper permissions

- **Missing dependencies?**
  - Run `pip install google-adk requests` again
  - Check that your virtual environment is activated

- **Weather not working?**
  - Ensure you have internet access
  - The weather API is public and doesn't require authentication

- **Google Search not working?**
  - The `google_search` tool requires proper setup
  - Check ADK documentation for Google Search tool configuration

### Debugging Tips
- Use the Dev UI's Events tab to inspect function calls and responses
- Check the Console tab for error messages
- Verify agent instructions are clear and specific

---

## Further Resources
- [ADK Documentation](https://google.github.io/adk-docs/get-started/quickstart/)
- [Google AI Studio](https://aistudio.google.com/app/apikey)
- [ADK GitHub](https://github.com/google/adk-python)
- [ADK Python API Reference](https://google.github.io/adk-docs/api-reference/python/index.html)

---

Happy agent building! 🎉
