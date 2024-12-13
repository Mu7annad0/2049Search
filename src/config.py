from dataclasses import dataclass

@dataclass
class Config:
    model_name = "gemma2:9b"
    embedding_model = "thenlper/gte-small"
    max_num_tokens = 1000
    tempreature = 0.0
    max_search_results = 7
    retrieved_docs_limits = 5
