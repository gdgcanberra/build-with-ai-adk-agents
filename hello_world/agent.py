from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.0-flash",
    
    # Provide a concise summary of the agent's capabilities. 
    # This description is primarily used by other LLM agents to determine if they should route a task to this agent. 
    # Make it specific enough to differentiate it from peers (e.g., "Handles inquiries about current billing statements," not just "Billing agent").
    description="You are a helpful assistant that can answer questions and help with tasks.",
    
    instruction="""You are a helpful assistant that can answer questions and help with tasks.""",
    tools=[],
)