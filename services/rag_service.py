# RAG implementation
import openai
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import tempfile
import os
from pathlib import Path
from config.settings import Settings

class RAGService:
    def __init__(self):
        openai.api_key = Settings.OPENAI_API_KEY
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Settings.CHUNK_SIZE,
            chunk_overlap=Settings.CHUNK_OVERLAP
        )
        self.vector_store = None
        self.qa_chain = None
        self._load_or_create_vector_store()
    
    def _load_or_create_vector_store(self):
        """Load existing vector store or create new one"""
        try:
            if Settings.VECTOR_DB_PATH.exists():
                self.vector_store = FAISS.load_local(
                    str(Settings.VECTOR_DB_PATH), 
                    self.embeddings
                )
            else:
                # Create empty vector store
                self.vector_store = FAISS.from_texts(
                    ["Welcome to the AI Assistant knowledge base"], 
                    self.embeddings
                )
                self._save_vector_store()
            
            # Initialize QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=OpenAI(temperature=0),
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 3})
            )
        except Exception as e:
            print(f"Vector store initialization error: {e}")
    
    def add_document(self, uploaded_file) -> bool:
        """
        Add document to knowledge base
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Success status
        """
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            
            # Load document based on file type
            if uploaded_file.name.endswith('.pdf'):
                loader = PyPDFLoader(tmp_path)
            else:
                loader = TextLoader(tmp_path, encoding='utf-8')
            
            documents = loader.load()
            
            # Split documents into chunks
            texts = self.text_splitter.split_documents(documents)
            
            # Add to vector store
            if self.vector_store:
                self.vector_store.add_documents(texts)
            else:
                self.vector_store = FAISS.from_documents(texts, self.embeddings)
            
            # Save updated vector store
            self._save_vector_store()
            
            # Clean up temporary file
            os.unlink(tmp_path)
            
            return True
            
        except Exception as e:
            print(f"Document processing error: {e}")
            return False
    
    def get_response(self, query: str) -> str:
        """
        Get RAG-enhanced response to query
        
        Args:
            query: User query
            
        Returns:
            AI response based on knowledge base
        """
        try:
            if self.qa_chain:
                response = self.qa_chain.run(query)
                return response
            else:
                return "Knowledge base not available. Please add some documents first."
        except Exception as e:
            print(f"RAG query error: {e}")
            return "Sorry, I couldn't process your query at the moment."
    
    def _save_vector_store(self):
        """Save vector store to disk"""
        try:
            Settings.VECTOR_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            self.vector_store.save_local(str(Settings.VECTOR_DB_PATH))
        except Exception as e:
            print(f"Vector store save error: {e}")
    
    def get_stats(self) -> dict:
        """Get knowledge base statistics"""
        try:
            if self.vector_store:
                return {
                    'document_count': len(self.vector_store.docstore._dict),
                    'chunk_count': self.vector_store.index.ntotal,
                    'vector_dims': self.vector_store.index.d
                }
            return {'document_count': 0, 'chunk_count': 0, 'vector_dims': 0}
        except Exception as e:
            print(f"Stats error: {e}")
            return {'document_count': 0, 'chunk_count': 0, 'vector_dims': 0}
