import os
from types import SimpleNamespace
from typing import Any
from dotenv import load_dotenv

load_dotenv()

try:
    from crewai import Agent as CrewAgent, Task as CrewTask  # type: ignore
except Exception:  # pragma: no cover - crewai may not be available
    CrewAgent = None
    CrewTask = None


class StubAgent(SimpleNamespace):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.role = kwargs.get('role', '')
        self.goal = kwargs.get('goal', '')
        self.backstory = kwargs.get('backstory', '')
        self.tools = kwargs.get('tools', [])
        self.memory = kwargs.get('memory', False)
        self.verbose = kwargs.get('verbose', False)
        self.allow_delegation = kwargs.get('allow_delegation', False)
        self.max_iter = kwargs.get('max_iter')
        self.max_execution_time = kwargs.get('max_execution_time')


class StubTask(SimpleNamespace):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.description = kwargs.get('description', '')
        self.agent = kwargs.get('agent')
        self.expected_output = kwargs.get('expected_output', '')
        self.context = kwargs.get('context', '')
        self.output_file = kwargs.get('output_file')
        self.config = kwargs.get('config', {})
    
    def get(self, key, default=None):
        """Implement get method for compatibility with CrewAI"""
        return getattr(self, key, default)


def _crewai_available() -> bool:
    # First check if CrewAI is actually importable
    if CrewAgent is None or CrewTask is None:
        print("⚠️  CrewAI not available - using stub agents")
        return False
    
    # Check for any available LLM configuration
    has_openai = bool(os.getenv('OPENAI_API_KEY'))
    has_ollama = bool(os.getenv('OLLAMA_BASE_URL'))
    
    if not (has_openai or has_ollama):
        print("⚠️  No LLM configured - using stub agents")
        return False
    
    # Check if we should use simulators (force stub mode)
    use_simulators = os.getenv('USE_SIMULATORS', 'false').lower() == 'true'
    if use_simulators:
        print("⚠️  Simulator mode enabled - using stub agents")
        return False
    
    # Test if we can actually create a CrewAI agent
    try:
        # Test agent creation with minimal config
        test_agent = CrewAgent(
            role='Test Agent',
            goal='Test goal',
            backstory='Test backstory'
        )
        print("✅ CrewAI available and functional - using real agents")
        return True
    except Exception as e:
        print(f"⚠️  CrewAI import failed: {e}")
        print("   Using stub agents")
        return False


def create_agent(**kwargs: Any) -> Any:
    if _crewai_available():
        try:
            return CrewAgent(**kwargs)
        except Exception as e:
            print(f"⚠️  CrewAgent creation failed: {e}")
            print("   Falling back to StubAgent")
    return StubAgent(**kwargs)


def create_task(**kwargs: Any) -> Any:
    if _crewai_available():
        try:
            return CrewTask(**kwargs)
        except Exception as e:
            print(f"⚠️  CrewTask creation failed: {e}")
            print("   Falling back to StubTask")
    return StubTask(**kwargs)
