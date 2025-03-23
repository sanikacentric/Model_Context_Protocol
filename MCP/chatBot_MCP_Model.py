from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import requests

# Set OpenAI API Key
OPENAI_API_KEY = "your-openai-api-key"

# Set Google Maps API Key
GOOGLE_MAPS_API_KEY = "your-google-maps-api-key"

# Initialize LangChain OpenAI LLM
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)

###  Functions for External APIs (Google Maps & Wikipedia)

def google_maps_search(location):
    """Search for a location using Google Maps API."""
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": location, "key": GOOGLE_MAPS_API_KEY}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else {"error": "Google Maps API failed"}

def wikipedia_search(query):
    """Search Wikipedia for information."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {"error": "Wikipedia API failed"}

###  Define MCP Model (Routing Queries)

mcp_routes = {
    "GoogleMapSearchAgent": ["where is", "location of", "find place", "search place"],
    "WikiSearchAgent": ["who is", "what is", "tell me about", "history of"]
}

### 🚀 LangChain-Powered Query Routing

def mcp_route_query(user_query):
    """Routes query to the appropriate LLM agent based on intent using LangChain."""
    
    # Determine the correct agent based on keywords
    selected_agent = "WikiSearchAgent"  # Default
    for agent, keywords in mcp_routes.items():
        if any(keyword in user_query.lower() for keyword in keywords):
            selected_agent = agent
            break

    print(f"🔄 MCP Routing to {selected_agent}...")

    # Create structured messages for LLM using LangChain
    messages = [
        SystemMessage(content=f"Route the query to the correct agent: {selected_agent}."),
        HumanMessage(content=user_query)
    ]

    # Call LangChain's LLM for response generation
    llm_response = llm(messages).content
    print(f"🤖 {selected_agent}: {llm_response}")

    # Call external API based on selected agent
    if selected_agent == "GoogleMapSearchAgent":
        api_result = google_maps_search(user_query)
    else:
        api_result = wikipedia_search(user_query)

    # Format the API response and print it
    print("🌍 API Result:", api_result)

###  Example User Queries
mcp_route_query("Where is the Eiffel Tower?")
mcp_route_query("Who is Albert Einstein?")
