# 🏨 tphagent User Guide

## 📱 How to Use the tphagent App

The tphagent (Hotel Sales Multi-Agent System) is a powerful AI-powered tool that helps hotels optimize their marketing through automated Google Ads campaign creation, market research, and performance optimization.

---

## 🎯 Main User Interfaces

### 1. **Command Line Interface (CLI)**
- Direct terminal/command prompt interaction
- Simple commands for immediate results
- Perfect for quick analysis and testing

### 2. **Python API Integration**
- Programmatic access for developers
- Custom integration capabilities
- Batch processing support

### 3. **Custom Diagnosis Input**
- Personalized hotel analysis
- Flexible input formats
- Real-world problem solving

### 4. **Test Mode**
- System health verification
- Component testing
- Troubleshooting support

### 5. **Configuration Management**
- Multiple integration levels
- Environment customization
- Service configuration

---

## 🚀 Quick Start Methods

### **METHOD 1: Run with Sample Data**
```bash
python main.py
```
- **Description**: Uses built-in sample diagnosis
- **Output**: Complete marketing strategy
- **Best For**: First-time users, testing

### **METHOD 2: Test System Components**
```bash
python main.py test
```
- **Description**: Tests all system components
- **Output**: System health report
- **Best For**: Troubleshooting, verification

### **METHOD 3: Custom Hotel Diagnosis**
1. Edit `main.py`
2. Replace `sample_diagnosis` with your data
3. Run `python main.py`
- **Output**: Personalized marketing strategy
- **Best For**: Real hotel analysis

### **METHOD 4: Python API Integration**
```python
from main import run_diagnosis_workflow

# Your hotel diagnosis
diagnosis = "Your hotel marketing challenge here..."

# Run the analysis
result = run_diagnosis_workflow(diagnosis)
```
- **Output**: Structured results for integration
- **Best For**: Developers, automation

---

## 📊 Input Formats

### **Hotel Diagnosis Format**
Your input should include:
- **Current occupancy rate**: XX%
- **Average daily rate**: $XXX
- **Competitor pricing**: $XXX
- **Main issues**: [list problems]
- **Goals**: [specific objectives]
- **Location**: [city, country]
- **Target audience**: [guest segments]

### **Example Input**
```
Low weekend occupancy for boutique hotel in Miami.
Current: 45% occupancy, target: 75%.
ADR: $180, competitors: $220.
Issues: Weak digital presence, poor keyword targeting.
Goal: Increase occupancy and ADR through Google Ads.
```

---

## 📁 Output Deliverables

### **Generated Files**
- 📄 `market_research_report.md` - Market analysis
- 📄 `google_ads_campaign.md` - Campaign strategy
- 📄 `optimization_report.md` - Performance recommendations
- 📄 `workflow_results.json` - Complete results
- 📄 `memory.pkl` - Learning data

### **Report Contents**
- Market trends and competitor analysis
- Keyword research and targeting
- Ad copy and campaign structure
- Budget allocation and bidding strategies
- Performance optimization recommendations

---

## ⚙️ Configuration Levels

### **Level 1: Basic (Simulator Mode)**
- ✅ Local LLM (Ollama)
- ✅ File-based memory
- ✅ Google Ads simulator
- ❌ No external APIs required
- **Best For**: Learning, testing, development

### **Level 2: Enhanced (Pinecone + Simulator)**
- ✅ Local LLM (Ollama)
- ✅ Pinecone vector storage
- ✅ Google Ads simulator
- ✅ Advanced memory capabilities
- **Best For**: Advanced users, better memory

### **Level 3: Production (Full Integration)**
- ✅ Local LLM (Ollama)
- ✅ Pinecone vector storage
- ✅ Real Google Ads API
- ✅ Complete production capabilities
- **Best For**: Professional use, live campaigns

---

## 🎯 Use Cases

### **1. Hotel Marketing Managers**
- Generate complete Google Ads campaigns
- Get market research and competitor analysis
- Receive optimization recommendations

### **2. Digital Marketing Agencies**
- Automate campaign creation for hotel clients
- Scale marketing strategy development
- Standardize optimization processes

### **3. Hotel Owners/Operators**
- Understand market positioning
- Get actionable marketing strategies
- Learn from performance data

### **4. Marketing Consultants**
- Rapidly analyze hotel marketing challenges
- Generate comprehensive strategies
- Provide data-driven recommendations

---

## 🔄 Workflow Process

### **Step 1: Input Hotel Diagnosis**
- Describe current situation
- Specify goals and challenges
- Provide context and location

### **Step 2: AI Agent Processing**
- **Market Researcher**: Analyzes trends
- **Ad Generator**: Creates campaigns
- **Optimizer**: Provides recommendations
- **Supervisor**: Ensures quality

### **Step 3: Output Generation**
- Comprehensive reports created
- Campaign strategies developed
- Optimization plans provided
- Results saved to files

### **Step 4: Implementation**
- Use generated Google Ads campaigns
- Follow optimization recommendations
- Monitor performance metrics
- Iterate based on results

---

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.8+
- Ollama (for local LLM) - [Install from ollama.ai](https://ollama.ai/)
- Pinecone account (optional) - [Sign up at pinecone.io](https://www.pinecone.io/)
- Google Ads API access (optional) - [Get credentials](https://ads.google.com/)

### **Quick Setup**
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
   cp .env.example .env
   nano .env  # Edit with your API keys
   ```

### **Manual Setup**
1. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Ollama**:
   ```bash
   ollama serve
   ollama pull llama3.1:8b
   ```

---

## 🎉 Ready to Use!

The tphagent app is ready for hotel marketing optimization! Choose your preferred method and start generating results!

### **Next Steps**
1. Choose your configuration level
2. Set up your environment
3. Run your first analysis
4. Review the generated reports
5. Implement the recommendations

**Happy optimizing! 🚀**