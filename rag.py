from langchain_qdrant import QdrantVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import Document
from qdrant_client import models
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_together import Together
from langchain_core.prompts import PromptTemplate
from utils import open_ai_prompt

class RagModel():
    def __init__(self, api_keys, qdrant_api_key, qdrant_url, qdrant_collection_name,
                embedding_model, architecture = "", model="meta-llama/Meta-Llama-3.1-8B-Instruct", number_of_doc = 3):
        self.apikeys = api_keys
        self.qdrant_api_key = qdrant_api_key
        self.qdrant_url = qdrant_url
        self.qdrant_collection_name = qdrant_collection_name
        self.architecture = architecture
        self.model = model
        self.number_of_doc = number_of_doc
        if architecture == "openai":
            self.embedding = OpenAIEmbeddings(model = embedding_model,
                                               api_key = api_keys)
        else:
            self.embedding = HuggingFaceEmbeddings(model_name=embedding_model)

    def retrieve_data(self, user_input, resolved_ticket_flag):
        
        qdrant = QdrantVectorStore.from_existing_collection(
                            embedding = self.embedding,
                            collection_name = self.qdrant_collection_name,
                            url = self.qdrant_url,
                            api_key = self.qdrant_api_key,
                        )
        
        # THis is for metadata filtering. Only tickets which are Resolved will only be considered.
        if resolved_ticket_flag:
            filters = models.Filter(must=[models.FieldCondition(
                                key="metadata.Resolved",
                                match=models.MatchValue(value=True),
                            ),])
            qdrant_retriever = qdrant.as_retriever(search_type="similarity", search_kwargs={"k": self.number_of_doc, "filter": filters})
        else:
            qdrant_retriever = qdrant.as_retriever(search_type="similarity", search_kwargs={"k": self.number_of_doc})
            

        if self.architecture == "openai":
            template = open_ai_prompt()
            llm = ChatOpenAI(model=self.model, api_key = self.apikeys)
        else:
            template = (                           
                        """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
                        You are an IT helpdesk assistant designed to assist support agents by suggesting solutions to technical issues based on past tickets - "Resolution".
                        Your task is to analyze the user entered ticket details and generate a resolution suggestion based on the past retrieved context tickets.
                        Past retrieved tickets will have an Issue, Description and Resolution. 
                        
                        GUIDELINES:
                        1. Provide ONLY resolution suggestion based ONLY on retrieved context.
                        2. Never answer from your knowledge.
                        3. Keep the answer short and to the point by avoiding unnecessary explanations.
                        4. If the user question cannot be answered with the retrieved context respond strictly with: "No relevant similar ticket found for resolution suggestion"
                        5. Avoid repetitive steps—ensure a structured approach.
                    
                        {context}
                        <|eot_id|>\n<|begin_of_text|><|start_header_id|>user<|end_header_id|>
                        Based ONLY on the provided tickets, suggest possible solution to the following question:
                        Question: {input}
                        Helpful Answer:
                        <|eot_id|>\n<|begin_of_text|><|start_header_id|>assistant<|end_header_id|>"""
                        )
            llm = Together(model=self.model, api_key = self.apikeys, temperature = 0.0)

        prompt = PromptTemplate(
            template=template, input_variables=["context", "input"]
        )

        
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        # This first retrieves relevant documents (past tickets) and merges retrieved docs into the prompt 
        # and then formats them into a query prompt for the llm
        rag_chain = create_retrieval_chain(qdrant_retriever, question_answer_chain)
        rag_response = rag_chain.invoke({"input": user_input})
        return rag_response 
    
    def upload_data(self, data):
        docs = []
        for _, row in data.iterrows():
            content = f"Issue: {row['Issue']}\n  Description: {row['Description']}\n  Resolution: {row['Resolution']}"
            
            doc = Document(page_content=content,
                           metadata={"Ticket ID": row["Ticket ID"], "Category": row["Category"],
                                    "Agent Name": row["Agent Name"], "Date": row["Date"], "Resolved": row["Resolved"],
                                    "Resolution": row['Resolution']})
            docs.append(doc)
        new_collection_name = "ticket_collection_huggingface_78"
        qdrant = QdrantVectorStore.from_documents(
                    docs,
                    embedding = self.embedding,
                    url = self.qdrant_url,
                    prefer_grpc=True,
                    api_key = self.qdrant_api_key,
                    collection_name = new_collection_name,
                )
        
        return new_collection_name