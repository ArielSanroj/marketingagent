"""
Hybrid Memory System for Hotel Sales Agents
Implements both short-term (CrewAI) and long-term (Pinecone) memory
"""
import os
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
import json
import pickle

try:
    from pinecone import Pinecone  # type: ignore
except Exception:  # pragma: no cover - best effort fallback for limited environments
    Pinecone = None

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:  # pragma: no cover - best effort fallback for limited environments
    SentenceTransformer = None

load_dotenv()

class HotelSalesMemory:
    """Hybrid memory system for storing and retrieving hotel sales data"""

    def __init__(self):
        self.index_name = 'hotel-sales-memory'
        self.embedding_dim = 384
        self._use_vector_store = False
        self._local_store: List[Dict[str, Any]] = []
        self.pc = None
        self.index = None
        self.embeddings = None
        self.memory_file = os.path.join(os.getenv('OUTPUT_DIR', 'outputs'), 'memory.pkl')
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        
        # Try to initialize Pinecone if available
        if Pinecone is not None and SentenceTransformer is not None and os.getenv('PINECONE_API_KEY'):
            try:
                self.pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
                self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
                self._setup_index()
                self.index = self.pc.Index(self.index_name)
                self._use_vector_store = True
                print("✅ Pinecone vector store initialized")
            except Exception as e:
                print(f"⚠️  Pinecone initialization failed: {e}")
                print("   This may be due to sentence-transformers compatibility issues")
                print("   Falling back to file-based memory storage")
                self._use_vector_store = False
                self.pc = None
                self.index = None
                self.embeddings = None
        else:
            if not os.getenv('PINECONE_API_KEY'):
                print("⚠️  PINECONE_API_KEY not set, using file-based memory")
            elif SentenceTransformer is None:
                print("⚠️  sentence-transformers not available, using file-based memory")
            elif Pinecone is None:
                print("⚠️  pinecone-client not available, using file-based memory")
        
        # Load existing file-based memory
        self._load_from_file()
    
    def _setup_index(self):
        """Create Pinecone index if it doesn't exist"""
        if not self._use_vector_store or self.pc is None:
            return

        try:
            if self.index_name not in self.pc.list_indexes().names():
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.embedding_dim,
                    metric='cosine',
                    spec={
                        "serverless": {
                            "cloud": "aws",
                            "region": os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')
                        }
                    }
                )
        except Exception as e:
            print(f"⚠️  Error setting up Pinecone index: {e}")
            self._use_vector_store = False
    
    def _load_from_file(self):
        """Load memory data from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'rb') as f:
                    self._local_store = pickle.load(f)
                print(f"✅ Loaded {len(self._local_store)} memories from file")
            except Exception as e:
                print(f"⚠️  Error loading memory file: {e}")
                self._local_store = []
        else:
            self._local_store = []
    
    def _save_to_file(self):
        """Save memory data to file"""
        try:
            with open(self.memory_file, 'wb') as f:
                pickle.dump(self._local_store, f)
        except Exception as e:
            print(f"⚠️  Error saving memory file: {e}")
    
    def save_to_memory(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Save content to long-term memory with embeddings"""
        metadata = dict(metadata or {})
        metadata.update({
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'type': metadata.get('type', 'hotel_sales_data')
        })

        memory_id = str(uuid.uuid4())

        if self._use_vector_store and self.index is not None and self.embeddings is not None:
            try:
                embedding = self.embeddings.encode(content).tolist()
                self.index.upsert(vectors=[(memory_id, embedding, metadata)])
                return f"Successfully saved to memory with ID: {memory_id}"
            except Exception as e:
                return f"Error saving to memory: {str(e)}"

        self._local_store.append({
            'id': memory_id,
            'content': content,
            'metadata': metadata,
            'score': 1.0
        })
        self._save_to_file()
        return f"Stored locally with ID: {memory_id}"
    
    def retrieve_from_memory(self, query: str, top_k: int = 5,
                             filter_metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Retrieve relevant memories based on query"""
        filter_metadata = filter_metadata or {}

        if self._use_vector_store and self.index is not None and self.embeddings is not None:
            try:
                query_embedding = self.embeddings.encode(query).tolist()
                results = self.index.query(
                    vector=query_embedding,
                    top_k=top_k,
                    include_metadata=True,
                    filter=filter_metadata
                )

                memories = []
                for match in results.get('matches', []):
                    memories.append({
                        'id': match.get('id'),
                        'score': match.get('score'),
                        'content': match.get('metadata', {}).get('content', ''),
                        'metadata': {
                            k: v for k, v in match.get('metadata', {}).items() if k != 'content'
                        }
                    })

                return memories
            except Exception as e:
                print(f"Error retrieving from memory: {str(e)}")

        query_lower = query.lower() if query else None
        results = []
        for entry in reversed(self._local_store):
            if filter_metadata and any(entry['metadata'].get(k) != v for k, v in filter_metadata.items()):
                continue

            if query_lower and query_lower not in entry['content'].lower():
                continue

            results.append({
                'id': entry['id'],
                'score': entry['score'],
                'content': entry['content'],
                'metadata': {
                    k: v for k, v in entry['metadata'].items() if k != 'content'
                }
            })

            if len(results) >= top_k:
                break

        return results
    
    def search_by_type(self, content_type: str, query: str = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search memories by specific type (e.g., 'ad_performance', 'market_trends')"""
        filter_metadata = {'type': content_type}
        
        if query:
            return self.retrieve_from_memory(query, top_k, filter_metadata)
        else:
            # Get all memories of this type
            return self.retrieve_from_memory("", top_k, filter_metadata)
    
    def save_ad_performance(self, campaign_id: str, metrics: Dict[str, Any]) -> str:
        """Save Google Ads performance data"""
        content = f"Campaign {campaign_id} performance: {json.dumps(metrics, indent=2)}"
        metadata = {
            'type': 'ad_performance',
            'campaign_id': campaign_id,
            'metrics': metrics
        }
        return self.save_to_memory(content, metadata)
    
    def save_market_trends(self, trends: Dict[str, Any]) -> str:
        """Save market research and trend data"""
        content = f"Market trends analysis: {json.dumps(trends, indent=2)}"
        metadata = {
            'type': 'market_trends',
            'analysis_date': datetime.now().isoformat()
        }
        return self.save_to_memory(content, metadata)
    
    def save_guest_insights(self, insights: Dict[str, Any]) -> str:
        """Save guest behavior and preference insights"""
        content = f"Guest insights: {json.dumps(insights, indent=2)}"
        metadata = {
            'type': 'guest_insights',
            'analysis_date': datetime.now().isoformat()
        }
        return self.save_to_memory(content, metadata)
    
    def get_recent_performance(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get recent ad performance data"""
        # This would typically filter by date range
        return self.search_by_type('ad_performance', top_k=10)
    
    def get_market_insights(self) -> List[Dict[str, Any]]:
        """Get latest market trend insights"""
        return self.search_by_type('market_trends', top_k=5)
    
    def get_guest_insights(self) -> List[Dict[str, Any]]:
        """Get latest guest behavior insights"""
        return self.search_by_type('guest_insights', top_k=5)

# Global memory instance
memory = HotelSalesMemory()