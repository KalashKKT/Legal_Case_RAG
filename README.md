# Legal_Case_RAG
Here's a **README** description for your **Legal RAG App** project:  

---

# **Legal RAG App – Indian Penal Code (IPC) Legal Assistant**  

## **Overview**  
The **Legal RAG App** is a **Retrieval-Augmented Generation (RAG)** system designed to assist legal professionals, law students, and individuals in finding relevant **Indian Penal Code (IPC)** sections for legal cases. It utilizes **FastAPI** for API interaction, **FAISS** for vector database storage, and **Groq's LLaMA-3** as the language model.  

## **Features**  
✅ **Legal Document Processing** – Loads and splits IPC legal text from a CSV file.  
✅ **Efficient Information Retrieval** – Uses **FAISS vector database** for fast similarity search.  
✅ **High-Quality Embeddings** – Utilizes **Hugging Face MiniLM-L6-v2** for embedding creation.  
✅ **RAG-Based Answering** – Integrates a **RetrievalQA Chain** for context-aware responses.  
✅ **FastAPI Integration** – Provides a REST API for querying legal cases.  

## **Tech Stack**  
- **Programming Language**: Python  
- **Libraries**:  
  - **LangChain** (RetrievalQA, FAISS, Embeddings)  
  - **Hugging Face Embeddings**  
  - **Groq Chat (LLaMA-3)**  
  - **FastAPI** (Backend API)  
  - **FAISS** (Vector Search Engine)  
  - **Uvicorn** (ASGI Server)  

## **Installation & Setup**  

1️⃣ **Clone the repository**  
```bash
git clone https://github.com/KalashKKT/Legal_Case_RAG.git
cd Legal_Case_RAG
```

2️⃣ **Install dependencies**  
```bash
pip install -r requirements.txt
```

3️⃣ **Set up environment variables**  
Create a `.env` file and add:  
```
GROQ_API="your_groq_api_key"
```

4️⃣ **Run the FastAPI server**  
```bash
python IPC_RAG_App.py
```

5️⃣ **Access the API**  
- Visit **http://localhost:8000/docs** for API documentation.  
- Send a **POST request** to `http://localhost:8000/chain` with a **JSON payload**:  
```json
{
    "query": "What IPC sections apply for financial fraud?"
}
```

## **How It Works**  
1. Loads **IPC sections from a CSV file**.  
2. Splits the text into smaller **context-aware chunks**.  
3. Generates **embeddings** using **Hugging Face MiniLM-L6-v2**.  
4. Stores embeddings in a **FAISS vector database**.  
5. Uses **Groq LLaMA-3** to process legal queries with **retrieval-augmented generation (RAG)**.  
6. Provides **accurate legal sections** based on the retrieved context.  

## **Example Response**  
```json
{
    "result": "Based on the retrieved context, Section 420 of IPC applies to financial fraud cases.",
    "source_documents": ["Section 420 - Cheating and dishonestly inducing delivery of property..."]
}
```

## **Future Enhancements**  
🔹 Expand the dataset with more legal codes and case precedents.  
🔹 Improve retrieval accuracy with better embeddings.  
🔹 Implement multi-model support for legal research.  

---
