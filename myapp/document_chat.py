from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from .util import load_embeddings, load_db


load_dotenv()

class retrieval_chat():
    def __init__(self) -> None:
        embedding_function = load_embeddings()
        db = load_db(embedding_function)
        self.qa = RetrievalQA.from_llm(llm=ChatOpenAI(temperature=0.1), retriever=db.as_retriever(kwargs={"k": 7}), return_source_documents=True)

    def answer_question(self, question: str):
        output = self.qa({"query": question})
        # source_documents_str = ", ".join(map(str, output["source_documents"]))
        # print("Source Documents: " + source_documents_str)
        return output["result"]

if __name__ == "__main__":
    qa = retrieval_chat()
    while True:
        print("What's Your Question:")
        query = input()
        
        print(qa.answer_question(query))

