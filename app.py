import streamlit as st
from agent import agent_executor # We import the brain you just built!

st.set_page_config(page_title="Competitor Spy", page_icon="🕵️‍♂️")

# Custom CSS to make it look "Hacker Mode"
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #1E1E1E;
        color: #00FF00;
        border: 1px solid #00FF00;
    }
    .stButton > button {
        width: 100%;
        background-color: #00FF00;
        color: black;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🕵️‍♂️ Competitor Spy Agent")
st.caption("Powered by Llama-3.3, LangGraph & Custom Scrapers")

# Input Section
target_url = st.text_input("Enter Competitor Name or URL", placeholder="e.g. 'Linear' or 'www.jasper.ai'")

if st.button("🚀 INFILTRATE & ANALYZE"):
    if not target_url:
        st.warning("Please enter a target!")
    else:
        # Create a status container
        status_box = st.status("Initializing Agent...", expanded=True)
        
        try:
            # 1. Construct the prompt
            query = f"""
            1. Search for {target_url} to find their official homepage URL.
            2. Use the scrape_website tool to read their homepage.
            3. Analyze their value proposition and pricing if available.
            4. Summarize their top 3 selling points in a bulleted list.
            """
            
            # 2. Run the Agent (and update status)
            status_box.write("🔍 Searching for target...")
            
            # LangGraph returns a dictionary of messages. We want the last one.
            response = agent_executor.invoke({"messages": [("user", query)]})
            final_answer = response["messages"][-1].content
            
            status_box.update(label="✅ Mission Complete", state="complete", expanded=False)
            
            # 3. Display Result
            st.subheader("📂 Mission Report")
            st.markdown(final_answer)
            
        except Exception as e:
            status_box.update(label="❌ Mission Failed", state="error")
            st.error(f"Error: {str(e)}")