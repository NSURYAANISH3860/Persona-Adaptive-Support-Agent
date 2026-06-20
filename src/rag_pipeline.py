import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
import chromadb
from src.config import GEMINI_API_KEY, EMBEDDING_MODEL, CHROMA_DB_DIR

class LocalRAGPipeline:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.collection = self.chroma_client.get_or_create_collection(name="support_kb")

    def get_embedding(self, text: str) -> list:
        response = self.client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text
        )
        return response.embeddings[0].values

    def load_and_ingest_all(self, data_dir="data"):
        for filename in os.listdir(data_dir):
            filepath = os.path.join(data_dir, filename)
            content = ""
            
            if filename.endswith((".txt", ".md")):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            elif filename.endswith(".pdf"):
                reader = PdfReader(filepath)
                for page in reader.pages:
                    content += page.extract_text() + "\n"
            
            if content:
                self.ingest_document(filename, content)

    def ingest_document(self, doc_name: str, content: str):
        splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)
        chunks = splitter.split_text(content)

        for idx, chunk in enumerate(chunks):
            embedding = self.get_embedding(chunk)
            chunk_id = f"{doc_name}_chunk_{idx}"
            
            self.collection.upsert(
                ids=[chunk_id],
                embeddings=[embedding],
                metadatas=[{"source": doc_name, "chunk_index": idx}],
                documents=[chunk]
            )

    def retrieve_context(self, query: str, top_k: int = 2) -> list:
        query_vector = self.get_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )

        retrieved_items = []
        if results and results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                distance = results['distances'][0][i] if results['distances'] else 0.0
                retrieved_items.append({
                    "text": results['documents'][0][i],
                    "source": results['metadatas'][0][i]['source'],
                    "score": 1.0 - distance 
                })
        return retrieved_items