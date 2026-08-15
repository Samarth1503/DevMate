import logging
from typing import Any

import chromadb

from services.vector_store import VectorStore

logger = logging.getLogger(__name__)


class ChromaService(VectorStore):
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="devmate_docs")
        logger.info("ChromaDB initialized.")

    async def add_document(
        self, doc_id: str, text: str, metadata: dict[str, Any] = None
    ):
        try:
            self.collection.add(
                documents=[text], metadatas=[metadata or {}], ids=[doc_id]
            )
        except Exception as e:
            logger.error(f"Error adding document to ChromaDB: {e}")

    async def search(self, query: str, n_results: int = 5) -> list[dict[str, Any]]:
        try:
            results = self.collection.query(query_texts=[query], n_results=n_results)

            # Format the output
            formatted_results = []
            if results["documents"] and len(results["documents"]) > 0:
                for i in range(len(results["documents"][0])):
                    formatted_results.append(
                        {
                            "id": results["ids"][0][i],
                            "document": results["documents"][0][i],
                            "metadata": results["metadatas"][0][i]
                            if results["metadatas"]
                            else {},
                        }
                    )
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching ChromaDB: {e}")
            return []


vector_store = ChromaService()
