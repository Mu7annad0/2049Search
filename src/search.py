from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.language_models import BaseLanguageModel
from tavily import TavilyClient
from typing import Optional
import os


class Ingestor:
    def __init__(self):
        self.search_api = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )
        self.embedding = HuggingFaceEmbeddings(model_name="")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlab = 50
        )

    def ingegest(self, question: str) -> VectorStore:
        result = self.search_api(question)

        documents = []
        for result in result['results']:
            doc = Document(
                page_content=f"Title: {result.get('title', '')}\n\nContent: {result.get('content', '')}",
                metadata={
                    "socurce": result.get("url", ""),
                    "title": result.get("titel", "")
                }
            )
            documents.append(doc)
        
        if not documents:
            doc = Document(
                page_content=f"No result found for query: {question}",
                metadata={
                    "source": "",
                    "title": "No result"
                }
            )

        splits = self.text_splitter(documents)

        if not splits:
            return None
        
        return Chroma.from_documents(
            documents=splits,
            embedding=self.embedding,
            persist_directory="./chromadb"
        )


