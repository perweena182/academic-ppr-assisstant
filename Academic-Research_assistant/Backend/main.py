from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.search_agent import SearchAgent
from agents.db_agent import DBAgent
from agents.qa_agent import QAAgent
from agents.future_works_agent import FutureWorksAgent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:8501",  # Streamlit's default port
    "http://127.0.0.1:8501",
]


# Allow CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # Adjust this in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
search_agent = SearchAgent()
db_agent = DBAgent()
qa_agent = QAAgent()
future_works_agent = FutureWorksAgent()

class TopicRequest(BaseModel):
    topic: str

class QueryRequest(BaseModel):
    topic: str
    query: str

# Add this to main.py
@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.post("/search")
def search_papers(request: TopicRequest):
    try:
        papers = search_agent.search(request.topic)
        db_agent.store_papers(request.topic, papers)
        print("stored")
        return {"papers": papers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/qa")
def answer_question(request: QueryRequest):
    try:
        answer = qa_agent.answer(request.topic, request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
def summarize_papers(request: TopicRequest):
    try:
        summary = qa_agent.summarize(request.topic)
        
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_review")
def generate_review(request: TopicRequest):
    try:
        review = future_works_agent.generate_review(request.topic)
        return {"review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
