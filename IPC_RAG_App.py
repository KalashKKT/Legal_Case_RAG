import os 
from dotenv import load_dotenv
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate , SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain.chains import RetrievalQA , LLMChain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain

from pydantic import BaseModel
from fastapi import FastAPI , HTTPException
import uvicorn

#loader instance
loader = CSVLoader('ipc_sections.csv',encoding="utf-8")
#loading the documents from Csv file
doc = loader.load()

#splitting the data 
splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
chunks = splitter.split_documents(doc)

#embedding the data
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#Storing into Vector Data Base
db_faiss = "faiss_db"
db = FAISS.from_documents(chunks, embeddings)
db.save_local(db_faiss)
print("Saved into the vector database")

# Loading a LLm 
GROQ_API_KEY = os.getenv("GROQ_API")
llm = ChatGroq(
   model_name="llama3-8b-8192",
   api_key= GROQ_API_KEY)

# Creating the ChatPromptTemplate
chat_prompt_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "As a legal assistant specializing in criminal law in the Indian Penal Code (IPC), your task is to identify applicable legal sections relevant to the provided scenario. Below is the user's query. List all applicable legal sections for the scenario. If the provided context does not contain sufficient information to determine the relevant sections, respond with 'I'm unable to provide an answer based on the available information.'"
    ),
    HumanMessagePromptTemplate.from_template(
        "Context: {context}\n\nQuery: {question}"
    )
])

#loading the stored vector DB
db_faiss = "faiss_db"
db = FAISS.load_local(db_faiss,
                      embeddings,
                      allow_dangerous_deserialization=True)



# Retrieval QA Chain
qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 10}),
                                       return_source_documents=True,
                                       verbose = True,
                                       chain_type_kwargs={'prompt': chat_prompt_template}
                                        )


#5. Create FastAPI app
app = FastAPI(title="Legal_Rag_App",
              description="Answer to all your legal cases queries",
              version="0.1")

# Define the QueryRequest model
class QueryRequest(BaseModel):
    query: str 

#fastAPI endpoint
@app.post("/chain")
async def query_chain(request: QueryRequest):
    try:
        # Pass the user's query to the RetrievalQA chain
        result = qa_chain({"query": request.query})
        return {"result": result["result"], "source_documents": result.get("source_documents", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)