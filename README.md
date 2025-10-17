# Hotel Sales Multi-Agent System

A sophisticated multi-agent system built with CrewAI for hotel sales optimization, featuring Google Ads campaign creation and management. This system implements the unified framework from "A Survey on Large Language Model based Autonomous Agents" with specialized agents for market research, ad generation, performance optimization, and quality supervision.

## 🏗️ Architecture

The system follows a modular architecture with four specialized agents:

- **Market Researcher**: Analyzes hospitality trends, guest segments, and keyword opportunities
- **Ad Generator**: Creates compelling Google Ads campaigns and ad copy
- **Performance Optimizer**: Optimizes campaigns based on performance data
- **Supervisor**: Coordinates the team and ensures quality control

## 🚀 Features

- **Hybrid Memory System**: Short-term (CrewAI) and long-term (Pinecone) memory
- **Google Ads Integration**: Campaign creation, management, and optimization
- **Multi-Agent Collaboration**: Sequential workflow with delegation capabilities
- **Performance Analytics**: Real-time campaign performance tracking
- **Quality Control**: Automated review and approval processes

## 📋 Prerequisites

- Python 3.8+
- Ollama (for local LLM) - [Install from ollama.ai](https://ollama.ai/)
- Pinecone account (optional) - [Sign up at pinecone.io](https://www.pinecone.io/)
- Google Ads API access (optional for simulation) - [Get credentials](https://ads.google.com/)

### Dependencies

The system automatically installs required Python packages:
- `crewai` - Multi-agent framework
- `langchain` - LLM integration
- `pinecone-client` - Vector database
- `google-ads` - Google Ads API
- `sentence-transformers` - Embeddings (optional)
- `python-dotenv` - Environment management

## 🛠️ Installation

### Quick Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd tphagent
   ```

2. **Run the setup script**:
   ```bash
   python setup_integration.py
   ```

3. **Edit environment variables**:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env file with your API keys
   nano .env
   ```

### Manual Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Install and configure Ollama** (optional):
   ```bash
   # Install Ollama from https://ollama.ai/
   ollama serve
   ollama pull llama2
   # Or use mistral: ollama pull mistral
   ```

## 🔧 Configuration

### Environment Variables

The system now supports multiple integration levels:

#### Required (Minimal Setup)
- **Ollama**: Local LLM (recommended for development)
- **File-based memory**: Automatic fallback

#### Optional (Full Functionality)
- **Pinecone**: Vector database for advanced memory
- **Google Ads API**: Real campaign management
- **OpenAI**: Alternative to Ollama

Create a `.env` file with your configuration:

```env
# LLM Configuration (Ollama - Recommended)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_API_KEY=your_ollama_api_key

# CrewAI Configuration (to use Ollama with CrewAI)
OLLAMA_OPENAI_API_KEY=your_ollama_api_key
OLLAMA_OPENAI_API_BASE=http://localhost:11434/v1
OLLAMA_OPENAI_MODEL_NAME=llama3.1:8b

# Alternative LLM (Optional)
# OPENAI_API_KEY=your_openai_api_key

# Pinecone Vector Database (Optional - falls back to file storage)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1

# Google Ads API (Optional - falls back to simulator)
GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token
GOOGLE_ADS_CLIENT_ID=your_client_id
GOOGLE_ADS_CLIENT_SECRET=your_client_secret
GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token
GOOGLE_ADS_LOGIN_CUSTOMER_ID=your_login_customer_id

# System Configuration
USE_SIMULATORS=false  # Set to true to use simulators only
DEBUG=false           # Set to true for debug logging
```

### Configuration Levels

The system supports different levels of integration:

#### 1. Basic Mode (Ollama + Simulators)
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_API_KEY=your_key_here
USE_SIMULATORS=true
```
- ✅ Local LLM with Ollama
- ✅ File-based memory storage
- ✅ Google Ads simulator
- ❌ No Pinecone integration
- ❌ No real Google Ads API

#### 2. Enhanced Mode (Ollama + Pinecone)
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_API_KEY=your_key_here
PINECONE_API_KEY=your_pinecone_key
USE_SIMULATORS=true
```
- ✅ Local LLM with Ollama
- ✅ Pinecone vector storage
- ✅ Google Ads simulator
- ❌ No real Google Ads API

#### 3. Full Production Mode (All Services)
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_API_KEY=your_key_here
PINECONE_API_KEY=your_pinecone_key
GOOGLE_ADS_DEVELOPER_TOKEN=your_token
# ... other Google Ads credentials
USE_SIMULATORS=false
```
- ✅ Local LLM with Ollama
- ✅ Pinecone vector storage
- ✅ Real Google Ads API integration
- ✅ Full production capabilities

### Configuration Levels

The system supports different levels of integration:

#### 1. Basic Mode (Ollama + Simulators)
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_API_KEY=your_key_here
USE_SIMULATORS=true
```
- ✅ Local LLM with Ollama
- ✅ File-based memory storage
- ✅ Google Ads simulator
- ❌ No Pinecone integration
- ❌ No real Google Ads API

#### 2. Enhanced Mode (Ollama + Pinecone)
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_API_KEY=your_key_here
PINECONE_API_KEY=your_pinecone_key
USE_SIMULATORS=true
```
- ✅ Local LLM with Ollama
- ✅ Pinecone vector storage
- ✅ Google Ads simulator
- ❌ No real Google Ads API

#### 3. Full Production Mode (All Services)
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_API_KEY=your_key_here
PINECONE_API_KEY=your_pinecone_key
GOOGLE_ADS_DEVELOPER_TOKEN=your_token
# ... other Google Ads credentials
USE_SIMULATORS=false
```
- ✅ Local LLM with Ollama
- ✅ Pinecone vector storage
- ✅ Real Google Ads API integration
- ✅ Full production capabilities

### Service Setup

#### Pinecone Setup (Optional)
1. Create a Pinecone account at https://www.pinecone.io/
2. Create a new project
3. Get your API key and environment
4. Add them to your `.env` file

#### Google Ads API Setup (Optional)
1. Create a Google Ads account
2. Set up API access in Google Ads API Center
3. Get your developer token and OAuth credentials
4. Add them to your `.env` file

## 🎯 Usage

### Basic Usage

Run the system with a sample diagnosis:

```bash
python main.py
```

### Test Mode

Test the system components:

```bash
python main.py test
```

### Custom Diagnosis

Modify the `sample_diagnosis` in `main.py` with your specific hotel data:

```python
sample_diagnosis = """
Your hotel diagnosis here...
Current occupancy rate: XX%
Average daily rate: $XXX
Main issues: [list issues]
Goal: [your goals]
"""
```

## 📁 Project Structure

```
tphagent/
├── agents/                 # Agent definitions
│   ├── researcher.py      # Market research agent
│   ├── ad_generator.py    # Ad creation agent
│   ├── optimizer.py       # Performance optimization agent
│   └── supervisor.py      # Quality control agent
├── tasks/                 # Task definitions
│   ├── research_task.py   # Market research task
│   ├── ad_generation_task.py  # Ad creation task
│   └── optimization_task.py   # Optimization task
├── utils/                 # Utility functions
│   ├── memory.py          # Memory management
│   └── google_ads.py      # Google Ads integration
├── main.py               # Main orchestration
├── config.py             # Configuration settings
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## 🔄 Workflow

1. **Market Research**: Agent analyzes market trends and identifies opportunities
2. **Ad Generation**: Agent creates targeted Google Ads campaigns
3. **Optimization**: Agent optimizes campaigns based on performance data
4. **Supervision**: Agent reviews and approves all outputs

## 🧪 Testing

The system includes comprehensive testing capabilities:

### Integration Tests
```bash
python test_integrations.py
```

Tests include:
- Environment configuration validation
- Memory system (Pinecone + file fallback)
- Google Ads integration (real API + simulator)
- CrewAI compatibility layer
- Output file creation
- LLM integration (Ollama/OpenAI)
- Full workflow execution

### Component Tests
```bash
python component_test.py
python standalone_test.py
python simple_test.py
```

### Test Coverage
- Memory system validation
- Google Ads simulator testing
- Agent workflow testing
- Performance metrics validation
- File output generation
- Error handling and fallbacks

## 📊 Outputs

The system generates comprehensive output files in the `outputs/` directory:

### Generated Reports
- `market_research_report.md`: Market analysis and insights
- `google_ads_campaign.md`: Campaign configuration and ad copy
- `optimization_report.md`: Performance optimization recommendations
- `workflow_results.json`: Complete workflow results

### Logs
- `logs/workflow_log_*.json`: Detailed execution logs
- `outputs/memory.pkl`: Persistent memory storage (file-based fallback)

### File Structure
```
outputs/
├── market_research_report.md
├── google_ads_campaign.md
├── optimization_report.md
├── workflow_results.json
└── memory.pkl

logs/
└── workflow_log_YYYYMMDD_HHMMSS.json
```

## 🔧 Customization

### Adding New Agents

1. Create a new agent file in `agents/`
2. Define the agent with appropriate role, goal, and backstory
3. Add the agent to the crew in `main.py`

### Adding New Tasks

1. Create a new task file in `tasks/`
2. Define the task with description and expected output
3. Add the task to the crew workflow

### Customizing Memory

Modify `utils/memory.py` to add new memory types or retrieval methods.

## 🚀 Deployment

### Local Development

The system is designed to run locally with Ollama for the LLM.

### Cloud Deployment

For production deployment:

1. Use a cloud-based LLM (OpenAI, Anthropic, etc.)
2. Deploy Pinecone for vector storage
3. Set up Google Ads API integration
4. Use Docker for containerization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:

1. Check the documentation
2. Review the test outputs
3. Check the logs in the `logs/` directory
4. Open an issue on GitHub

## 🔮 Future Enhancements

- Real Google Ads API integration
- Additional marketing channels (Facebook, Instagram)
- Advanced analytics dashboard
- Multi-hotel support
- Automated reporting
- Integration with hotel management systems

---

Built with ❤️ using CrewAI and the Unified Agent Framework