from abc import ABC, abstractmethod
from typing import Any


class VectorStore(ABC):
    @abstractmethod
    async def add_document(
        self, doc_id: str, text: str, metadata: dict[str, Any] = None
    ):
        """Add a document to the vector store."""
        pass

    @abstractmethod
    async def search(self, query: str, n_results: int = 5) -> list[dict[str, Any]]:
        """Search the vector store for similar documents."""
        pass
