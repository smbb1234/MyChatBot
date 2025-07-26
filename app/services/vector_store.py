from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain.schema.document import Document
from .embedding import get_embedding_model

class QdrantStore:
    """
    A class to interact with Qdrant for storing and retrieving documents.
    It uses LangChain's QdrantStore for efficient document management and retrieval.
    """
    def __init__(
            self,
            host: str = "localhost",
            port: int = 6333,
            collection_name: str = "rag_docs",
            embedding_model = None
    ):
        self.collection_name = collection_name
        self.client = QdrantClient(host=host, port=port)
        self.embedding_model = embedding_model if embedding_model else get_embedding_model()

        self.qdrant_client = QdrantClient(
            host=host,
            port=port
        )

        # Connect to the Qdrant collection using the provided embedding model.
        if not self.qdrant_client.collection_exists(self.collection_name):
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self._get_vector_dim(),
                    distance=Distance.COSINE
                )
            )

        self.vectorstore = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=self.collection_name,
            embedding=self.embedding_model
        )

    def _get_vector_dim(self) -> int:
        """
        Dynamically obtain embedding dimensions.
        """
        dummy_vector = self.embedding_model.embed_documents(["test"])[0]
        return len(dummy_vector)

    def add_documents(self, docs: List[Document]):
        """Add a list of documents to the Qdrant collection.
        Each document should have a 'page_content' attribute.
        """
        self.vectorstore.add_documents(documents=docs)

    def get_retriever(self, k: int = 5):
        """
        Returns the LangChain Retriever interface for use by the RAG process
        """
        return self.vectorstore.as_retriever(search_kwargs={"k": k})

    def delete_all(self):
        """
        Delete the current collection
        """
        self.qdrant_client.delete_collection(self.collection_name)

if __name__ == "__main__":
    store = QdrantStore(collection_name="test")

    docs = [
        Document(page_content="The Eiffel Tower is in Paris."),
        Document(page_content="The Colosseum is in Rome."),
        Document(page_content="The Great Wall is in China."),
    ]
    store.add_documents(docs)

    retriever = store.get_retriever(k=2)
    # invoke the retriever with a query
    results = retriever.invoke("Where is the Eiffel Tower?")

    print("\nTop Relevant Documents:")
    for i, doc in enumerate(results):
        print(f"{i + 1}: {doc.page_content}")
    # This code defines a QdrantStore class that interacts with a Qdrant database to store and retrieve documents based on vector embeddings.
    # It uses LangChain's QdrantVectorStore for integration with LangChain's retriever interface, allowing for efficient document management and retrieval based on vector similarity.
    # The class includes methods for adding documents and retrieving them using a query vector.
    # The example at the end demonstrates how to use the QdrantStore with an embedding model and retrieve relevant documents based on a query.
