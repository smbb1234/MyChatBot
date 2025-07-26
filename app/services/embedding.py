from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model(model_name="all-MiniLM-L6-v2") -> HuggingFaceEmbeddings:
    """
    Embedding model using HuggingFace embeddings.
    Returns a LangChain compatible embedding model object.
    By default, 'all-MiniLM-L6-v2' is used, and the output is a 384-dimensional vector.
    """
    return HuggingFaceEmbeddings(model_name=model_name)

if __name__ == "__main__":
    model = get_embedding_model()
    vectors = model.embed_documents(["Test sentence 1", "Test sentence 2"])
    print(vectors)
#   This code defines an embedding model using HuggingFace embeddings.
#   It initializes the model and provides a method to embed documents.
#   The main block demonstrates how to use the model to embed a list of sentences.
#   The output will be a list of vectors representing the embedded documents.
#   This is useful for tasks like semantic search or document similarity.
