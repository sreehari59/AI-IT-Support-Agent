import streamlit as st
import openai  # For LLM-generated responses
from sentence_transformers import SentenceTransformer
# import faiss
import numpy as np
import pandas as pd

# Load model & database (Assuming embeddings are precomputed)
model = SentenceTransformer("all-MiniLM-L6-v2")
# index = faiss.read_index("ticket_embeddings.index")  # Load vector DB
index = 0
past_tickets = pd.read_csv("data/ticket_dump_1.csv")

st.set_page_config(page_title="AI Helpdesk Assistant", layout="wide")

# Sidebar - User input
st.sidebar.title("🔍 Search for a Solution")
ticket_description = st.sidebar.text_area("Describe the issue", placeholder="Enter the problem details...")
category = st.sidebar.selectbox("Category", ["General", "Software", "Hardware", "Network"], index=0)
search_button = st.sidebar.button("🔎 Find Solution")

# Main Display
st.title("AI Helpdesk Assistant 🛠️")

if search_button and ticket_description:
    # Generate query embedding
    # query_embedding = model.encode(ticket_description).reshape(1, -1)

    # Search in FAISS vector database
    # D, I = index.search(query_embedding, 3)  # Retrieve top 3 matches

    st.subheader("🔗 Relevant Past Tickets")
    # for rank, idx in enumerate(I[0]):
    #     if idx == -1:
    #         continue
        # st.markdown(f"**#{rank+1} Ticket**")
        # st.info(f"📌 **Issue:** {past_tickets[idx]['Issue']}\n✅ **Resolution:** {past_tickets[idx]['Resolution']}\n🔗 **Ticket ID:** {past_tickets[idx]['id']}")
    
    st.markdown(f"**#{0+1} Ticket**")
    st.info(f"📌 **Issue:** {past_tickets['Issue'][0]}\n✅ **Resolution:** {past_tickets['Resolution'][0]}\n🔗 **Ticket ID:** {past_tickets['Ticket ID'][0]}")

    st.markdown(f"**#{0+1} Ticket**")
    st.info(f"📌 **Issue:** {past_tickets['Issue'][0]}\n✅ **Resolution:** {past_tickets['Resolution'][0]}\n🔗 **Ticket ID:** {past_tickets['Ticket ID'][0]}")


    # Generate LLM response
    st.subheader("🤖 AI-Suggested Response")
    prompt = f"Given this issue:\n{ticket_description}\nProvide a suggested resolution based on past tickets:\n"
    # response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    
    # suggested_solution = response["choices"][0]["message"]["content"]
    suggested_solution = "COme lets do this"
    editable_response = st.text_area("Modify Response Before Sending:", suggested_solution, height=200)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("📋 Copy to Clipboard")
    with col2:
        st.button("📤 Send to Ticket System")

    # Feedback section
    st.subheader("📢 Was this helpful?")
    feedback = st.radio("", ["👍 Yes", "👎 No"], horizontal=True)
    if feedback == "👎 No":
        st.text_area("What was wrong?", placeholder="Your feedback here...")
        st.button("Submit Feedback")

# Footer
st.markdown("---")
st.caption("Powered by AI | Streamlining IT Helpdesks 🚀")

