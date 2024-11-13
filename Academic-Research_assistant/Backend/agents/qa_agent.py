from models.llm_model import LLMModel
from agents.db_agent import DBAgent

class QAAgent:
    def __init__(self):
        self.llm = LLMModel()
        self.db_agent = DBAgent()

    def answer(self, topic, query):
        papers = self.db_agent.query_papers(topic)
        context = "\n".join([f"{paper['title']} ({paper['published']}): {paper['url']}" for paper in papers])
        prompt = f"Answer the following question elaborately based on these papers:\n{context}\n\nQuestion: {query}\nAnswer:"
        answer = self.llm.generate_text(prompt, task="qa")
        print(answer)
        return answer

    def summarize(self, topic):
        papers = self.db_agent.query_papers(topic)
        print(papers)
        context = "\n".join([f"{paper['title']} ({paper['published']}): {paper['url']}" for paper in papers])
        print(context)
        prompt = f"Summarize the research contributions on the topic '{topic}' from the past five years based on these papers:\n{context}\n\nSummary:"
        
        summary = self.llm.generate_text(prompt, task="summarization")
        return summary