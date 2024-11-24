from langchain_community.document_loaders import PyPDFLoader, UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.filters import EmbeddingsClusteringFilter
from typing import List, Optional
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentSummarizer:
    def __init__(
        self,
        model_name: str = "llama2",
        embedding_model: str = "all-MiniLM-L6-v2",
        num_clusters: int = 10,
        chunk_size: int = 2000,
        chunk_overlap: int = 200,
    ):
        self.llm = Ollama(model=model_name)
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.num_clusters = num_clusters
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.filter = EmbeddingsClusteringFilter(
            embeddings=self.embeddings, num_clusters=self.num_clusters
        )

    def extract_text(self, file_path: str) -> List:
        """Extract text from document with appropriate loader based on file type."""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension == ".pdf":
                loader = PyPDFLoader(file_path)
            else:
                loader = UnstructuredFileLoader(file_path)

            pages = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
            )

            texts = text_splitter.split_documents(pages)
            logger.info(f"Extracted {len(texts)} text chunks from {file_path}")
            return texts

        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            raise

    def summarize(self, file_path: str, custom_prompt: Optional[str] = None) -> str:
        """Summarize document using clustering and LLM."""
        try:
            # Extract and cluster text
            texts = self.extract_text(file_path)
            clustered_docs = self.filter.transform_documents(documents=texts)

            # Prepare the summarization chain
            if custom_prompt:
                prompt = custom_prompt
            else:
                prompt = """
                Write a comprehensive summary of the following text. 
                Focus on the main points and key insights.
                Use clear and concise language.
                
                Text: {text}
                """

            chain = load_summarize_chain(self.llm, chain_type="stuff", prompt=prompt)

            # Generate summary
            summary = chain.run(clustered_docs)
            return summary

        except Exception as e:
            logger.error(f"Error summarizing document: {str(e)}")
            raise


def main():
    # Example usage
    summarizer = DocumentSummarizer(
        model_name="llama2",
        embedding_model="all-MiniLM-L6-v2",
        num_clusters=10,
        chunk_size=2000,
        chunk_overlap=200,
    )

    try:
        file_path = "python.pdf"
        summary = summarizer.summarize(file_path)
        print("Document Summary:")
        print(summary)

    except Exception as e:
        logger.error(f"Failed to summarize document: {str(e)}")


if __name__ == "__main__":
    main()
