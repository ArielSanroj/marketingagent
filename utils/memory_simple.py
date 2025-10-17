"""
Simplified memory system for the Hotel Sales Multi-Agent System
Uses basic text storage without vector embeddings for compatibility
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class SimpleMemory:
    """Simplified memory system using JSON file storage"""
    
    def __init__(self):
        self.memory_file = "memory_data.json"
        self.memories = self._load_memories()
    
    def _load_memories(self) -> List[Dict[str, Any]]:
        """Load memories from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def _save_memories(self):
        """Save memories to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memories, f, indent=2)
    
    def save_to_memory(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Save content to memory"""
        memory_id = f"memory_{len(self.memories) + 1}_{int(datetime.now().timestamp())}"
        
        memory_entry = {
            'id': memory_id,
            'content': content,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        
        self.memories.append(memory_entry)
        self._save_memories()
        
        return memory_id
    
    def retrieve_from_memory(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve memories based on query (simple text matching)"""
        query_lower = query.lower()
        
        # Simple text matching
        matching_memories = []
        for memory in self.memories:
            content_lower = memory['content'].lower()
            if query_lower in content_lower:
                matching_memories.append(memory)
        
        # Sort by timestamp (most recent first)
        matching_memories.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return matching_memories[:top_k]
    
    def search_by_type(self, memory_type: str) -> List[Dict[str, Any]]:
        """Search memories by type"""
        matching_memories = []
        for memory in self.memories:
            if memory.get('metadata', {}).get('type') == memory_type:
                matching_memories.append(memory)
        
        return matching_memories
    
    def get_all_memories(self) -> List[Dict[str, Any]]:
        """Get all memories"""
        return self.memories
    
    def clear_memory(self):
        """Clear all memories"""
        self.memories = []
        self._save_memories()

# Create global memory instance
memory = SimpleMemory()