import streamlit as st
import pandas as pd
from dotenv import dotenv_values
import os
from rag import RagModel
from utils import response_generator, selectbox_styling, relevant_ticket_details
import warnings
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

selectbox_styling()
config = dotenv_values(".env")
new_df = pd.read_csv(config["NEW_DATA"])
new_df["Ticket-Issue"] = new_df["Ticket ID"] + " : " + new_df["Issue"]
print(new_df["Ticket-Issue"].values)

# Main Ttile
st.markdown("""
    <div style='text-align: center;'>
        <h1> AI IT Helpdesk Assistant 🛠️ </h1>
    </div>
""", unsafe_allow_html=True)

# Retrieves relevant ticket
def IT_Helpdesk():
    tickets = new_df["Ticket-Issue"].values

    ticket_issue = st.selectbox(
                        "Select Ticket : Issue",
                        (tickets),
                        index=None,
                        placeholder="Select Ticket ID and Issue",
                    )
    number_of_tickets = st.number_input("Number of Relevant Past ticket", value=3)
    resolved_tickets = st.checkbox("Tick to suggest only Resolved ticket")
    
    ticket_detail_flag = False
    ticket_assistance_flag = False
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Ticket Details"):
            ticket_detail_flag = True
            
    with col3:
        if st.button("🤖 AI Ticket Assistance"):
            ticket_assistance_flag =True
            

    if ticket_detail_flag:
        filtered_df = new_df[new_df["Ticket-Issue"] == ticket_issue] 
        df_melted = filtered_df.melt(var_name="Field", value_name="Value")
        st.write(df_melted)

    if ticket_assistance_flag:
        filtered_df = new_df[new_df["Ticket-Issue"] == ticket_issue] 
        df_melted = filtered_df.melt(var_name="Field", value_name="Value")
        st.write(df_melted)
        filtered_df.reset_index(inplace=True, drop=True)
      
        user_query = f"""Issue: {filtered_df["Issue"][0]}\n  Description: {filtered_df["Description"][0]}"""
        st.info(f"📌{user_query}")

        if config["ARCHITECTURE"] == "openai":
            api_key = config["OPEN_AI_API_KEY"]
            embedding_model = config["OPEN_AI_EMBEDDING_MODEL"]
            model = config["OPEN_AI_MODEL_NAME"]
        else:
            api_key = config["TOGETHER_AI_API_KEY"]
            embedding_model = config["HUGGING_FACE_EMBEDDING_MODEL"]
            model = config["TOGETHER_AI_MODEL_NAME"]

        rag = RagModel(api_key, config["QDRANT_API_KEY"], config["QDRANT_URL"], 
                        config["QDRANT_COLLECTION_NAME"], embedding_model, config["ARCHITECTURE"], model, number_of_tickets)
        
        response = rag.retrieve_data(user_query, resolved_tickets)
        # print(response)
        st.header("🔗 Relevant Past Tickets")

        with st.expander("🔗 Relevant Past Tickets"):
            relevant_ticket_details(response, number_of_tickets)

        resolution = response["answer"]
        # st.info(f"✅ **Resolution:** {resolution}")
        with st.chat_message("assistant"):
            st.write_stream(response_generator(resolution))

        st.subheader("📢 Was this helpful?")
        feedback = st.radio("Feedback", ["👍 Yes", "👎 No"], horizontal=True)
        print("Feedback was:",feedback)
            

# To upload new documents 
def Ticket_Uploader():
    uploaded_file = st.file_uploader(
                        "Upload the file", 
                        type = ["csv", "xlsx", "json"],
                        accept_multiple_files=False
                        )
    if st.button("Process Document"):
        if uploaded_file is not None:
            if ".csv" in uploaded_file.name:
                uploaded_df = pd.read_csv(uploaded_file)
            elif ".xlsx" in uploaded_file.name:
                uploaded_df = pd.read_excel(uploaded_file)
            elif ".json" in uploaded_file.name:
                uploaded_df = pd.read_json(uploaded_file)
            
            st.write(uploaded_df)
            if config["ARCHITECTURE"] == "openai":
                api_key = config["OPEN_AI_API_KEY"]
                embedding_model = config["OPEN_AI_EMBEDDING_MODEL"]
                model = config["OPEN_AI_MODEL_NAME"]
            else:
                api_key = config["TOGETHER_AI_API_KEY"]
                embedding_model = config["HUGGING_FACE_EMBEDDING_MODEL"]
                model = config["TOGETHER_AI_MODEL_NAME"]

            rag = RagModel(api_key, config["QDRANT_API_KEY"], config["QDRANT_URL"], 
                            config["QDRANT_COLLECTION_NAME"], embedding_model, config["ARCHITECTURE"], model)
            
            collection_name = rag.upload_data(uploaded_df)

            st.write("Document Processed Successfully")
            st.write("Uploded the data in :", collection_name)
    

pg = st.navigation([st.Page(IT_Helpdesk), st.Page(Ticket_Uploader)])
pg.run()

# For the foter
st.caption("Powered by AI | Streamlining IT Helpdesks 🚀")
