import os
from typing import Optional, Dict, Any

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


class Ingestor:
    """
    A class responsible for ingesting and processing search results.
    """

    def __init__(self):
        """
        Initialize the Ingestor with Tavily client, embedding model, and text splitter.
        """
        self.tavily_client = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
    
    def __init__embeddings(self):
        return HuggingFaceEmbeddings(model_name="thenlper/gte-small") 

    def ingest(self, question: str) -> VectorStore:
        """
        Ingest search results and create a vector store.

        Args:
            question (str): The search query.

        Returns:
            VectorStore: A vector store of processed documents or None if an error occurs.
        """
        try:
            result = self.tavily_client.search(question, max_results=6)

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

            splits = self.text_splitter.split_documents(documents)

            return Chroma.from_documents(
                documents=splits,
                embedding=self.__init__embeddings(),
                persist_directory="./chromadb"
            )
        except Exception as e:
            print(f"Error in ingest: {e}")
            return None


def retrievar(llm: BaseLanguageModel, vector_store: Optional[VectorStore]):
    """
    Create a retrieval chain for processing search queries.

    Args:
        llm (BaseLanguageModel): The language model to use for generating answers.
        vector_store (Optional[VectorStore]): The vector store to retrieve documents from.

    Returns:
        RetrievalQA: A retrieval chain that can process search queries.
    """
    template = """
    Relevant information:
    {context}
    Question: {question}
            
    Instructions:
    - Focus on clarity and ensure the response is easy to understand.
    - Structure the answer logically with an introduction, main points, and conclusion.
    - Ensure the information is relevant and accurate.
    - Use bullet points to clearly express the main points of the answer.
    - Present the response in a positive and engaging manner.

    Please provide a comprehensive and well-organized response using the above information.
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    retrieval_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(
            search_kwargs={"k": 5}
        ),
        verbose=True,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    return retrieval_chain


def _init_llm():
    """
    Initialize the language model.

    Returns:
        ChatOllama: Initialized language model or None if an error occurs.
    """
    try:
        return ChatOllama(
            model="gemma2:9b",
            temperature=0.0,
            max_tokens=1000
        )
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return None


class SearchEngine:

    def __init__(self):
        """
        Initialize the SearchEngine with a language model and ingestor.
        """
        self.llm = _init_llm()
        self.ingestor = Ingestor()

    def perform_search(self, question: str) -> Dict[str, Any]:
        """
        Perform a search for the given question.

        Args:
            question (str): The search query.

        Returns:
            Dict[str, Any]: A dictionary containing the search answer and sources.
        """
        try:
            db = self.ingestor.ingest(question)
            
            if db is None:
                return {
                    "answer": "Sorry, I couldn't find any relevant information.",
                    "sources": []
                }

            retrieval_chain = retrievar(self.llm, db)    
            result = retrieval_chain({"query": question})

            sources = []
            for doc in result["source_documents"]:
                source = {
                    "title": doc.metadata.get("title", ""),
                    "url": doc.metadata.get("source", "")
                }
                if source not in sources:
                    sources.append(source)
            
            return {
                "answer": result.get("result", "No answer found."),
                "sources": sources
            }
        except Exception as e:
            print(f"Error in perform_search: {e}")
            return {
                "answer": f"An error occurred: {str(e)}",
                "sources": []
            }


def main():
    """
    Main function to demonstrate search functionality.
    """
    query = "who is the head coach of manchester united now"
    search = SearchEngine()
    result = search.perform_search(query)
    print(result)


if __name__ == "__main__":
    # main()
    print()