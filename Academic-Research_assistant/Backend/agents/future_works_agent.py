from models.llm_model import LLMModel
from agents.db_agent import DBAgent

class FutureWorksAgent:
    def __init__(self):
        self.llm = LLMModel()
        self.db_agent = DBAgent()

    def generate_review(self, topic):
        papers = self.db_agent.query_papers(topic)
        context = "\n".join([f"{paper['title']} ({paper['published']}): {paper['url']}" for paper in papers])
        prompt = (
            f"Based on the following papers on '{topic}', generate a review paper summarizing key points and suggesting future research directions:\n{context}\n\nReview Paper:"
        )
        review = self.llm.generate_text(prompt, task="review")
        return review
        
