# Parallel Travel Planner Agent Workshop Guide

Welcome to the Build with AI - Hands-On workshop! In this guide, you'll learn how to build a multi-agent travel planner using the Google Agent Development Kit (ADK). This agent will gather restaurant, activity, and weather information for any destination, and synthesize it into a travel guide.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Install Dependencies](#install-dependencies)
4. [Authentication & API Keys](#authentication--api-keys)
5. [Code Walkthrough](#code-walkthrough)
6. [Running the Agent](#running-the-agent)
7. [Interacting with the Agent](#interacting-with-the-agent)
8. [Troubleshooting](#troubleshooting)
9. [Further Resources](#further-resources)

---

## Prerequisites
- **Python 3.9+** (recommended: 3.10 or 3.11)
- **pip** (Python package manager)
- **A code editor** (VS Code, PyCharm, etc.)
- **Terminal access**
- A [Google AI Studio](https://aistudio.google.com/app/apikey) or [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai) API key (see [Authentication](#authentication--api-keys))

---

## Project Setup
1. **Clone or create the project folder:**
   ```bash
   git clone <your-repo-url> adk-agents-build-with-ai
   cd adk-agents-build-with-ai
   ```
   Or create a new folder and navigate into it.

2. **Project structure:**
   Your folder should look like this:
   ```
   adk-agents-build-with-ai/
     parallel_agent/
       __init__.py
       agent.py
     README.md
   ```

---

## Install Dependencies
1. **(Recommended) Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install the required packages:**
   ```bash
   pip install google-adk requests
   ```
   - `google-adk` is the Agent Development Kit.
   - `requests` is used for weather API calls.

---

## Authentication & API Keys
To use Gemini models, you need an API key. There are two main options:

### Option 1: Google AI Studio (Recommended for most users)
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and create an API key.
2. In your project folder, create a file named `.env` inside `parallel_agent/`:
   ```bash
   touch parallel_agent/.env
   ```
3. Add the following lines to `parallel_agent/.env`:
   ```env
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_API_KEY_HERE
   ```
   Replace `PASTE_YOUR_ACTUAL_API_KEY_HERE` with your API key.

### Option 2: Google Cloud Vertex AI
1. Set up a Google Cloud project and enable Vertex AI.
2. Get your project ID and location.
3. In `parallel_agent/.env`, add:
   ```env
   GOOGLE_GENAI_USE_VERTEXAI=TRUE
   GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
   GOOGLE_CLOUD_LOCATION=YOUR_LOCATION
   ```

---

## Code Walkthrough
The main logic is in `parallel_agent/agent.py`. Here’s what each part does:

- **Imports:** Uses ADK’s agent classes and the Google Search tool.
- **Restaurant & Activities Agents:**
  - Use Google Search to find top restaurants and activities for a destination.
  - Each agent is specialized and only returns relevant results.
- **Weather Agent:**
  - Uses the Open-Meteo API to fetch a 3-day weather forecast for the city.
- **Parallel Agent:**
  - Runs the restaurant, activities, and weather agents simultaneously for fast information gathering.
- **Merger Agent:**
  - Synthesizes the results into a structured travel guide.
- **Pipeline:**
  - Runs the parallel agent, then the merger agent, to produce the final guide.
- **Root Agent:**
  - Entry point for user queries (e.g., "Plan a trip to Paris").

---

## Running the Agent

1. **Navigate to the project root:**
   ```bash
   cd /path/to/adk-agents-build-with-ai
   ```
2. **Launch the ADK Dev UI:**
   ```bash
   adk web
   ```
   - This will start a local web server (usually at http://localhost:8000).
   - If you don’t have the `adk` CLI, install it with:
     ```bash
     pip install google-adk[cli]
     ```

3. **Select your agent:**
   - In the Dev UI, select `parallel_agent` (or the name you used) from the dropdown.

4. **Chat with your agent:**
   - Try prompts like:
     - `Plan a trip to Tokyo`
     - `What should I do in Rome?`
     - `Give me a travel guide for Sydney`

---

## Interacting with the Agent
- The agent will return a travel guide with:
  - **Weather Overview**
  - **Recommended Restaurants**
  - **Things to Do**
  - **Daily Planning Suggestions**
- You can inspect function calls and responses in the Dev UI’s Events tab.

---

## Troubleshooting
- **Agent not showing in Dev UI?**
  - Make sure you’re running `adk web` from the project root (not inside `parallel_agent/`).
  - Check for typos in your agent’s name.
- **Authentication errors?**
  - Double-check your `.env` file and API key.
- **Missing dependencies?**
  - Run `pip install google-adk requests` again.
- **Weather not working?**
  - Ensure you have internet access (the weather agent uses a public API).

---

## Further Resources
- [ADK Documentation](https://google.github.io/adk-docs/get-started/quickstart/)
- [Google AI Studio](https://aistudio.google.com/app/apikey)
- [Vertex AI](https://cloud.google.com/vertex-ai)
- [ADK GitHub](https://github.com/google/adk-python)

---

Happy agent building! 🎉
