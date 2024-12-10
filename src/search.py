from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter

from tavily import TavilyClient
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
load_dotenv()


class Ingestor:
    def __init__(self):
        self.tavily_client = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )
        self.embedding = HuggingFaceEmbeddings(model_name="thenlper/gte-small")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 50
        )

    def ingest(self, question: str) -> VectorStore:
        try:
            result = self.tavily_client.search(question)

            documents = []
            for item in result['results']:
                doc = Document(
                    page_content=f"Title: {item.get('title', '')}\n\nContent: {item.get('content', '')}",
                    metadata={
                        "source": item.get("url", ""),
                        "title": item.get("title", "")
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
                documents.append(doc)

            splits = self.text_splitter.split_documents(documents)

            return Chroma.from_documents(
                documents=splits,
                embedding=self.embedding,
                persist_directory="./chromadb"
            )
        except Exception as e:
            print(f"Error in ingest: {e}")
            return None


def retrievar(llm: BaseLanguageModel, vector_store: Optional[VectorStore]):

    template = """
    Relevant Information: {context}
    Question: {question}

    provide a detailed answer using the above information.
    and include relevant citations.
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    return RetrievalQA.from_chain_type(
        llm = llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 4}),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )


def _init_llm():
    try: 
        return ChatOllama(
            model = "gemma2:9b",
            temperature = 0.0,
            max_tokens = 1000
        )
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return None
        

