# README

## Overview
This repository contains two web-based applications designed to assist users in efficiently accessing, analyzing, and managing academic research papers:
1. **Academic Research Paper Assistant**
2. **ArXiv Research Assistant: Advanced RAG with Graph Integration**

Both applications are structured with a **FastAPI** backend and a **Streamlit** frontend, leveraging modern technologies for advanced paper retrieval, summarization, and review generation.

---

## Project 1: Academic Research Paper Assistant

### Project Description
The Academic Research Paper Assistant is a comprehensive web application designed to streamline research tasks. Key functions include:
- **Paper Search**: Retrieve research papers relevant to specific topics.
- **Summarization**: Summarize research contributions.
- **Question-Answering**: Answer queries based on paper content.
- **Review Generation**: Generate review content and suggest future work based on research trends.

### System Components
1. **Backend (FastAPI)**:
    - **Endpoints**:
        - `/search`: Retrieves research papers for a specified topic.
        - `/qa`: Answers user questions about selected papers.
        - `/summarize`: Summarizes research contributions.
        - `/generate_review`: Creates review content based on a topic.
    - **Agents**:
        - **SearchAgent**: Interfaces with Arxiv for paper retrieval.
        - **DBAgent**: Manages Neo4j graph database to store and organize papers.
        - **LLMModel**: Uses T5 model for summarization and question answering.
    - **Database**:
        - **Neo4j**: Stores paper metadata, creating `Topic` and `Paper` nodes with `HAS_PAPER` relationships.

2. **Frontend (Streamlit)**:
    - User can input a topic to search for papers, view summaries, ask questions, and generate reviews.

### Usage
1. Run the FastAPI server.
2. Start the Streamlit application.
3. Use the interface to enter topics, view papers, and interact with them through chat.

---

## Project 2: ArXiv Research Assistant: Advanced RAG with Graph Integration

### Project Description
This application is aimed at providing an interactive, research-focused experience by combining Retrieval-Augmented Generation (RAG) and graph-based data integration for enhanced response accuracy and contextual depth.

### System Components
1. **Backend (FastAPI)**:
    - **Data Collection & Storage**:
        - Utilizes OAI-PMH to collect metadata from Arxiv, stores it in a vector database (Pinecone), and updates every 24 hours.
    - **Pipeline**:
        - **Vector Embedding**: Embeds paper metadata using Azure OpenAI.
        - **Knowledge Graph**: Builds a Neo4j graph database with relationships between topics and papers, allowing complex queries.
    - **Agents**:
        - **Metadata Collection**: Retrieves and cleans metadata for embedding.
        - **Query Handling**: Combines vector and graph searches to answer queries.
    - **Endpoints**:
        - `/search`, `/qa`, `/summarize`: Similar to the Academic Assistant but adds vector and graph-based querying.

2. **Frontend (Chainlit)**:
    - Provides a chat-based user interface for paper exploration, summary generation, and detailed question-answering.

### Usage
1. Start the FastAPI server and Chainlit interface.
2. Input a topic and navigate through relevant papers, summaries, and detailed responses.

---

## Technologies Used
- **FastAPI**: Backend server.
- **Streamlit/Chainlit**: Frontend interfaces.
- **Neo4j**: Graph database for relationship-based paper storage.
- **Pinecone**: Vector database for similarity-based searches.
- **T5 Language Model (Transformers)**: Summarization and question-answering.

## Key Differences
1. **Backend Architecture**:
   - **Academic Research Paper Assistant**: Focuses on research paper summarization and review generation from single or multiple papers.
   - **ArXiv Research Assistant**: Integrates RAG with graph querying to deliver deeper, context-aware responses.

2. **Frontend**:
   - **Academic Research Paper Assistant**: Streamlit-based interface, topic-specific paper interactions.
   - **ArXiv Research Assistant**: Chainlit provides a conversational interface with advanced paper retrieval.

---

## Getting Started
1. Clone this repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the FastAPI and Streamlit/Chainlit servers.
4. Access the frontend at the provided local address.

## Conclusion
Both applications provide distinct approaches to academic research, whether through summarization, question-answering, or advanced retrieval using RAG and graph databases. They represent powerful tools for enhancing research productivity and discovery.


