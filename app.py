import streamlit as st
from agent import agent_executor
from memory import save_to_memory, search_memory # <--- Added search_memory
from langchain_groq import ChatGroq # We need an LLM to answer chat questions

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
            
            # 2. Run the Agent
            status_box.write("🔍 Searching for target...")
            response = agent_executor.invoke({"messages": [("user", query)]})
            final_answer = response["messages"][-1].content
            
            # --- NEW: Save to Memory ---
            status_box.write("💾 Saving report to database...")
            save_to_memory(target_url, final_answer)
            # ---------------------------
            
            # Update status to success
            status_box.update(label="✅ Mission Complete & Saved", state="complete", expanded=False)
            
            # 3. Display Result
            st.subheader("📂 Mission Report")
            st.markdown(final_answer)
            
        except Exception as e:
            status_box.update(label="❌ Mission Failed", state="error")
            st.error(f"Error: {str(e)}")
            
# --- NEW SIDEBAR: Chat with Memory ---
st.sidebar.title("🧠 Group Intelligence")
st.sidebar.info("Ask questions about any company we have ever spied on.")

# 1. Chat Input
user_question = st.sidebar.text_area("Ask a question about saved competitors:", height=100)

if st.sidebar.button("Ask Memory"):
    if user_question:
        with st.sidebar.status("Thinking..."):
            # A. Retrieve relevant past reports from Pinecone
            context = search_memory(user_question)
            
            # B. Send to LLM to summarize
            # We use a simple direct call to the LLM here
            llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")
            
            prompt = f"""
            Based ONLY on the following context from our database, answer the user's question.
            
            CONTEXT:
            {context}
            
            USER QUESTION:
            {user_question}
            """
            
            answer = llm.invoke(prompt).content
            
        # C. Show Answer
        st.sidebar.markdown("### 💡 Answer")
        st.sidebar.markdown(answer)