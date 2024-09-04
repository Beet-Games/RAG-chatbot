import streamlit as st
from streamlit_chat import message
import getpass
import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
import json
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from uuid import uuid4
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec

#local imports
from prompts import contextualize_q_system_prompt, system_prompt 

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

#Chroma collection unique name
collection_name = os.getenv('COLLECTION_NAME')

#User ID and conversation ID for chat history
user_id = os.getenv('USER_ID')  
conversation_id = os.getenv('CONVERSATION_ID')

#Homepage URL to scrape content from
homepage = os.getenv('HOMEPAGE')
 
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
else:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize OpenAI Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Initialize a persistent Chroma client
persistent_client = chromadb.PersistentClient()

# Get or create a collection in Chroma
collection = persistent_client.get_or_create_collection(collection_name)

# Initialize the Chroma vector store from the client
vector_store = Chroma(
    client=persistent_client,
    collection_name=collection_name,
    embedding_function=embeddings,
)

# Check if documents are already added to the collection to avoid duplicates
existing_documents = collection.count()
print(f"Existing documents in the collection: {existing_documents}")
if existing_documents == 0:
    # Function to get all links from the homepage
    def get_links(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href and (href.startswith('http') or href.startswith('/')):
                full_url = urljoin(url, href)
                links.add(full_url)
        return links

    # Get links from the homepage
    links = get_links(homepage)

    # Remove any empty strings from the set
    links = {link for link in links if link}

    print("/nlinks", links)

    #Or we can load the links from a list of links if we already know from what links we want to get the information
    #to the user for example we already know the usueful links that can answer user questions from a hotel website

    # Load documents from the collected links
    loader = WebBaseLoader(web_paths=links)
    docs = loader.load()
    
    # Split documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=300)
    splits = text_splitter.split_documents(docs)

    # Prepare documents for adding to the vector store
    documents = [
        Document(page_content=split.page_content, metadata={"source": "web"}, id=str(uuid4()))
        for split in splits
    ]

    # Add documents to the vector store
    vector_store.add_documents(documents=documents)
    print("Vector store created and documents added successfully.")
else:
    print(f"Vector store already exists with {existing_documents} documents. No new documents added.")

# Create a retriever from the vector store
#retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 50})
#retriever = vector_store.as_retriever(search_type="similarity_score_threshold",search_kwargs={'score_threshold': 0.5, 'k': 50})
retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 50, "fetch_k": 100})
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Create a history-aware retriever
history_aware_retriever = create_history_aware_retriever(
    ChatOpenAI(model="gpt-4o"), retriever, contextualize_q_prompt
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Create a question-answering chain
question_answer_chain = create_stuff_documents_chain(ChatOpenAI(model="gpt-4o"), qa_prompt)

# Create a retrieval chain
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# Manage chat history statefully

def get_session_history(user_id: str, conversation_id: str):
    return SQLChatMessageHistory(f"{user_id}--{conversation_id}", "sqlite:///memory.db")

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
      history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user.",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
)   
st.set_page_config(page_title="CONAIR Chat", page_icon="💇")

# Hide Streamlit's default style elements
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize the session state variables for chat history and input field for UI elements
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'input_field' not in st.session_state:
    st.session_state['input_field'] = ''

def main():
    # Display a title and welcome message
    st.title("BIENVENIDO A CONAIR!")
    st.write("Sea cual sea tu look, lo tenemos cubierto. Si quieres saber más sobre nuestros productos, haz una pregunta.")

    response_container = st.container()
    container = st.container()
    with container:
        def submit():
            st.session_state['input_field'] = st.session_state['user_input']
            st.session_state['user_input'] = ''

        user_input = st.text_input("Pregunta aquí:", placeholder="¿Cómo puedo ayudarte hoy?", key='user_input', on_change=submit)
        user_input = st.session_state['input_field']

        # If user submits input, add to chat history and generate a response
        if user_input:
            response = conversational_rag_chain.invoke(
                {"input": user_input},  
                config={"configurable": {"user_id": user_id,"conversation_id": conversation_id}},
            )["answer"]
            st.session_state['chat_history'].append({"message": user_input, "is_user": True})
            st.session_state['chat_history'].append({"message": response, "is_user": False})

    # Container for displaying chat history to maintain a structured layout
    if st.session_state['chat_history']: 
        with response_container:
            for i, chat in enumerate(st.session_state['chat_history']):
                if chat['is_user']:
                    message(chat['message'], is_user=True, key=f"{i}_User")
                else:
                    message(chat['message'], is_user=False, key=f"{i}_AI")

# Run the main function
if __name__ == '__main__':
    main()


