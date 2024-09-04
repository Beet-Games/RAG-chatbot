# RAG-chatbot
A chatbot that can answer user questions about a given website using a Retrieval-Augmented Generation (RAG) approach.

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

## Installation
**Create a Virtual Environment (Optional but Recommended)**
To install and set up the chatbot, follow these steps:
1. Clone the repository: `git clone https://github.com/your-repo.git`
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
input:  "Hola me llamo Diego y estoy buscando productos en descuento para mi madre Beatriz.Dame las opciones que tienes"
Response: should respond with the available products that have a discount on the conair website with their prices before and after the discount.

input: "No le gusto el regalo a mi madre en que sucursal en la cuidad de mexico puedo hacer la devolucion?"
Response: Should respond with the conair store locations only in mexico city. 

input: "Recomiendame otro producto de connair para mi madre y creale una carta de dedicatoria con las caracteristicas del producto y agregale mi nombre y el nombre de mi madre a la carta" 
Response: Should respond with a product recommendation and a letter with the product details as well as the name of Diego's mothers and signed with the users name.

input:"Puedes hacerme un descuento en este producto?
Response: Should respond with a limitation of its capabilities. 






