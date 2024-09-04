# Implementing a Chatbot with RAG for Conair Mexico

Welcome to the README file for the implementation of a Chatbot with RAG (Retrieval-Augmented Generation) for Conair Mexico. This project aims to develop an intelligent chatbot that can assist users with their queries and provide relevant information about Conair products and services.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#Testing)


## Features
- Web Scraping: Scrapes a specified homepage to collect all accessible links for document extraction.
- Document Storage: Uses Chroma to store and manage documents with embedded vectors for similarity-based retrieval.
- Contextual Responses: RAG enables the chatbot to generate responses that are contextually aware and provide accurate information.
- Advanced Querying: Supports multiple retrieval strategies, including similarity, similarity score threshold, and Maximal Marginal Relevance (MMR).
- History: The chat bot uses a mechanism to load, save, and maintain conversational history using a mysql database.
- User and History Management: The history system can handle a user's UUID to track which user each conversation belongs to in MySQL. A user can have multiple conversations, each identified by a unique conversation ID. If a new conversation ID is assigned, the chat history will reset for that user

## Installation
**Create a Virtual Environment (Optional but Recommended)**
To install and set up the chatbot, follow these steps:
1. Clone the repository: `git clone https://github.com/Beet-Games/RAG-chatbot.git'
2. Install the required dependencies: `pip install -r requirements.txt`
3. Configure the chatbot settings: Update the configuration file with the necessary API keys and credentials look at the env.example for details.
4. The fist time the code is executed give the bot time to scrape the website and create the vector store with the extracted data. 


## Usage
To use the chatbot, follow these steps:
1. Launch the chatbot application with the following command 'streamlit run conair.py'.
2. Enter your query or question in the chat interface.
3. The chatbot will process your query and provide a relevant response.
4. Continue the conversation by asking additional questions or providing more information.

## Testing 
Test promt: 
- Input: `Hola, me llamo Diego y estoy buscando productos en descuento para mi madre Beatriz. Dame las opciones que tienes.'
Response: Should respond with the available products that have a discount on the Conair website, including their prices before and after the discount.

- Input: `Estoy interesado en saber más información sobre el producto 1.'
Response: Should respond with the characteristics of the first product from the list given in the previous response.

- Input: `¿Cómo lo podría ordenar?'
Response: Should respond with detailed steps on how to order a product on the Conair Mexico website.

- Input: `Recomiéndame otro producto de Conair para mi madre y créale una carta de dedicatoria con las características del producto. Agrega mi nombre y el nombre de mi madre a la carta.'
Response: Should respond with a different product recommendation and a letter with the product details, including Diego's mother's name and signed with Diego's name.