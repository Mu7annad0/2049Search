# Orbit.2049 Search Engine
Orbit.2049 is a simple Retrieval-Augmented Generation (RAG) search engine designed to provide detailed, accurate, and contextually enriched answers. It combines search results retrieved using the Tavily API with local processing powered by the Gemma2:9B language model, enhanced by vector embeddings and ChromaDB, to deliver comprehensive insights with reliable source citations.

## Preview
https://github.com/user-attachments/assets/356a6044-d84f-41ca-9c9d-5bdddaf7f71d


## Installation
1. Clone the Repository
    ```sh
    git clone git@github.com:Mu7annad0/2049Search.git
    cd 2049Search
    ```

2. Install the dependencies
    ```sh
    pip install -r requirements.txt
    ```

3. Install Ollama
    * https://ollama.com/

4. Download the model
    ```sh
    ollama pull gemma2
    ```

5. Run the model
    ```sh
    ollama serve
    ```

6. Sign-up in Tavily and get the API
   * https://tavily.com/

7. Add your api in the .env file
   ```sh
    TAVILY_API_KEY = "Add-your-api-key"
    ```

8. Run the application
    ```sh
    streamlit run src/app.py
    ```
