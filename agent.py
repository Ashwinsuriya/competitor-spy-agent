import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# 1. Load Secrets
load_dotenv()

# --- DEBUG BLOCK (DELETE AFTER FIXING) ---
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ ERROR: .env file not found or empty!")
    print(f"Current working directory: {os.getcwd()}")
    print("Please run the 'echo' command given in the chat.")
    exit()
else:
    print(f"✅ SUCCESS: API Key found (starts with {api_key[:10]}...)")
# -----------------------------------------

# 2. Define the Custom Tool
@tool
def scrape_website(url: str):
    """Scrape the content of a specific website url to read text. Input must be a valid http URL."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text[:5000] 
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

# 3. Setup the Brain (Llama 3 70B)
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile"
)

# 4. Equip the Tools
search_tool = DuckDuckGoSearchRun()
tools = [search_tool, scrape_website]

# 5. Create the Agent (LangGraph)
# This creates a compiled graph automatically
agent_executor = create_react_agent(llm, tools)

# 6. Run the Test
if __name__ == "__main__":
    print("🕵️‍♂️ Competitor Spy Agent Online (LangGraph Edition)...")
    target = input("Which company are we spying on? (e.g., 'Linear'): ")
    
    query = f"""
    1. Search for {target} to find their official homepage URL.
    2. Use the scrape_website tool to read their homepage.
    3. Analyze their value proposition and pricing if available.
    4. Summarize their top 3 selling points in a bulleted list.
    """
    
    # LangGraph expects a list of messages
    events = agent_executor.invoke({"messages": [("user", query)]})
    
    # The last message in the list is the AI's final answer
    print("\n--- MISSION REPORT ---")
    print(events["messages"][-1].content)