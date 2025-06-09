# 🤖 AI Deal Agent Framework

## 🎯 The Problem & Solution

### The Challenge

In today's fast-paced digital marketplace, finding genuine deals among thousands of daily offers is like finding a needle in a haystack. Traditional deal-hunting approaches face several critical limitations:

- **Information Overload**: Deal sites publish hundreds of offers daily across multiple categories
- **Price Validation Challenge**: It's nearly impossible to manually verify if a "deal" price represents genuine value
- **Time Intensive**: Manually scanning, evaluating, and comparing deals is extremely time-consuming
- **Missed Opportunities**: Great deals often expire quickly before discovery
- **Subjective Evaluation**: Human bias affects deal assessment and can lead to poor purchasing decisions

### Our Solution

The **AI Deal Agent Framework** revolutionizes deal discovery by deploying a sophisticated multi-agent AI system that:

🔍 **Automatically Discovers** deals from multiple RSS feeds across various product categories
🧠 **Intelligently Evaluates** prices using ensemble machine learning models and fine-tuned LLMs  
⚡ **Instantly Alerts** users when genuine opportunities are identified (>$50 savings)
📱 **Delivers Notifications** via SMS/WhatsApp for immediate action
🎯 **Eliminates False Positives** through rigorous AI-powered price validation

### Key Innovations

- **Ensemble Price Intelligence**: Combines 3 different AI models (fine-tuned LLM, RAG with vector similarity, Random Forest) for robust price estimation
- **Real-time Deal Curation**: Uses GPT-4 with structured outputs to filter and summarize only high-quality deals
- **Duplicate Prevention**: Memory system ensures users never receive alerts for previously seen deals
- **Scalable Architecture**: Multi-agent design allows easy addition of new deal sources and pricing models

### Impact

This system transforms deal hunting from a manual, time-intensive process into an **automated, intelligent service** that works 24/7 to identify genuine opportunities, allowing users to make informed purchasing decisions without the research overhead.

## Overview

The **AI Deal Agent Framework** is a sophisticated multi-agent system designed to automatically discover, evaluate, and alert users about lucrative deals from various online sources. The system combines multiple AI models, machine learning techniques, and real-time data processing to identify opportunities where products are priced significantly below their estimated market value.

## 🔄 Detailed Workflow

### Complete System Workflow

The AI Deal Agent Framework operates through a sophisticated 7-step workflow that runs continuously to identify lucrative deals:

#### Step 1: 🔍 **Multi-Source Deal Discovery**

The system uses **dual scanning approaches** for comprehensive deal coverage:

##### **Option A: Tavily Scanner** (🇮🇳 **Indian Market Focus**)

The **Tavily Scanner Agent** provides real-time Indian deal discovery:

- **AI-Powered Search**: Uses Tavily's intelligent search API to find current deals
- **Indian E-commerce Focus**: Targets major Indian platforms:

  - Flipkart (`flipkart.com`)
  - Amazon India (`amazon.in`)
  - Myntra (`myntra.com`)
  - Snapdeal (`snapdeal.com`)
  - Paytm Mall (`paytm.com`)
  - Tata CLiQ (`tatacliq.com`)

- **Smart Query Strategy**: Executes targeted searches for:

  - "best deals discounts electronics Flipkart Amazon India today"
  - "smartphone mobile phone offers discount India 2024"
  - "laptop computer deals Amazon India Flipkart sale"
  - "home appliances discount offers India electronics"

- **Real-time Results**: Fresh deal discovery with current pricing in INR (₹)
- **Market Relevance**: Products available for Indian consumers with local shipping

##### **Option B: RSS Scanner** (🌍 **International Backup**)

The **RSS Scanner Agent** monitors traditional feed sources:

- **Multi-Source Scraping**: Monitors 5 RSS feeds from DealNews covering:

  - Electronics (`/c142/Electronics/`)
  - Computers (`/c39/Computers/`)
  - Automotive (`/c238/Automotive/`)
  - Smart Home (`/f1912/Smart-Home/`)
  - Home & Garden (`/c196/Home-Garden/`)

- **Content Extraction**: For each RSS entry:

  - Fetches the full deal page using HTTP requests
  - Extracts detailed product information using BeautifulSoup
  - Parses title, summary, features, and pricing details
  - Cleans HTML content and normalizes text formatting

- **Memory Filtering**: Compares scraped deals against `memory.json` to avoid duplicate processing

##### **Intelligent Scanner Selection**

The **Planning Agent** intelligently chooses the best data source:

```python
# Prioritizes Indian deals when Tavily is available
if prefer_indian_deals and has_tavily:
    selection = tavily_scanner.scan(memory)  # Try Indian deals first
if not selection:
    selection = rss_scanner.scan(memory)     # Fallback to international
```

#### Step 2: 🧠 **AI-Powered Deal Curation**

The **Scanner Agent** uses OpenAI GPT-4o-mini with **Structured Outputs** to:

- **Quality Assessment**: Evaluates deals based on:

  - Description detail and clarity (4-5 sentence minimum)
  - Price clarity and confidence (must be explicit, not "% off")
  - Product specificity (avoids vague descriptions)

- **Content Standardization**:

  - Rephrases descriptions to focus on product features, not deal terms
  - Extracts numerical prices from various formats
  - Filters out deals with unclear or missing pricing

- **Top 5 Selection**: Returns the 5 most promising deals with detailed descriptions

#### 2b. **Tavily Scanner Agent** (`agents/tavily_scanner_agent.py`) 🆕

- **Role**: AI-powered Indian deal discovery
- **Color**: Cyan 🔵
- **Functions**:
  - Uses Tavily search API for real-time deal discovery
  - Targets major Indian e-commerce platforms (Flipkart, Amazon India, etc.)
  - Extracts INR pricing and local product availability
  - Provides fresh, market-relevant deals for Indian consumers

#### Step 3: 💰 **Multi-Model Price Estimation**

The **Ensemble Agent** coordinates three independent pricing models for robust estimation:

##### 3a. **Specialist Agent** (Fine-tuned LLM)

- **Model**: Llama 3.1 8B fine-tuned specifically for pricing
- **Hosting**: Modal cloud with GPU acceleration and 4-bit quantization
- **Approach**: Domain-specific price prediction based on product descriptions
- **Strengths**: Deep understanding of product value and market context

##### 3b. **Frontier Agent** (RAG-based)

- **Vector Search**: Uses ChromaDB with sentence transformer embeddings
- **Context Retrieval**: Finds 5 most similar products from training data
- **LLM Integration**: OpenAI/DeepSeek with retrieved context for informed pricing
- **Strengths**: Leverages similar product comparisons for accurate estimates

##### 3c. **Random Forest Agent** (Traditional ML)

- **Model**: scikit-learn Random Forest trained on vectorized descriptions
- **Features**: Sentence transformer embeddings (all-MiniLM-L6-v2)
- **Approach**: Statistical pattern recognition from product text
- **Strengths**: Baseline ML reliability and fast inference

#### Step 4: 🎯 **Ensemble Model Fusion**

The **Ensemble Agent** combines individual predictions using:

- **Linear Regression**: Trained weights for optimal model combination
- **Statistical Features**: Min, max, and individual predictions as inputs
- **Robust Output**: Weighted average that leverages each model's strengths
- **Validation**: Ensures non-negative price estimates

#### Step 5: 📊 **Opportunity Analysis**

The **Planning Agent** processes each deal to:

- **Discount Calculation**: `discount = estimated_price - deal_price`
- **Opportunity Ranking**: Sorts deals by discount amount (highest first)
- **Threshold Filtering**: Only considers deals with >$50 potential savings
- **Best Deal Selection**: Identifies the top opportunity from the batch

#### Step 6: 🚨 **Alert Generation & Notification**

When a qualifying opportunity is found, the **Messaging Agent**:

- **Multi-Channel Alerts**: Sends notifications via:

  - **SMS**: Direct text messages through Twilio
  - **WhatsApp**: Rich messaging with deal details
  - **Pushover**: Push notifications (optional)

- **Formatted Content**: Includes:

  - Product description summary
  - Current deal price vs estimated value
  - Discount amount and percentage
  - Direct link to the deal

- **Immediate Delivery**: Real-time notifications for time-sensitive deals

#### Step 7: 💾 **Memory Management & Persistence**

The system maintains state through:

- **Deal History**: Updates `memory.json` with processed deal URLs
- **Duplicate Prevention**: Ensures users never receive alerts for the same deal twice
- **Vector Database**: Persists ChromaDB embeddings for consistent similarity search
- **Model Caching**: Maintains warm Modal services to prevent cold starts

### Workflow Execution Modes

#### **Continuous Monitoring Mode**

```python
# Runs indefinitely, checking for new deals every cycle
while True:
    opportunities = planner.plan(memory=load_memory())
    if opportunities:
        save_to_memory(opportunities)
    time.sleep(scan_interval)
```

#### **Single Execution Mode**

```python
# One-time check for immediate opportunities
planner = PlanningAgent(collection)
opportunity = planner.plan(memory=load_memory())
```

### Performance Characteristics

- **Processing Speed**: ~2-3 minutes per complete workflow cycle
- **API Efficiency**: Batched processing minimizes API calls
- **Memory Usage**: Vector database cached locally for fast similarity search
- **Scalability**: Modal auto-scaling handles traffic spikes

### Error Handling & Reliability

- **Graceful Degradation**: System continues if individual models fail
- **API Fallbacks**: Switches between OpenAI and DeepSeek automatically
- **Network Resilience**: Retries failed HTTP requests with exponential backoff
- **Data Validation**: Strict type checking with Pydantic models

This workflow ensures that only high-quality, genuinely discounted deals reach users, while maintaining system reliability and performance efficiency.

## 🏗️ System Architecture

### Core Components

The framework consists of several specialized agents working in coordination:

#### 1. **Planning Agent** (`agents/planning_agent.py`)

- **Role**: Master orchestrator that coordinates all other agents
- **Color**: Green 🟢
- **Functions**:
  - Manages the complete workflow from deal discovery to notification
  - Coordinates between Scanner, Ensemble, and Messaging agents
  - Filters deals based on discount threshold ($50 minimum)
  - Prioritizes opportunities by discount amount

#### 2. **Scanner Agent** (`agents/scanner_agent.py`)

- **Role**: Deal discovery and content curation
- **Color**: Cyan 🔵
- **Functions**:
  - Scrapes RSS feeds from DealNews across multiple categories
  - Uses OpenAI GPT-4o-mini with structured outputs to select best deals
  - Filters deals based on description quality and price clarity
  - Avoids duplicate deals using memory system

#### 2b. **Tavily Scanner Agent** (`agents/tavily_scanner_agent.py`) 🆕

- **Role**: AI-powered Indian deal discovery
- **Color**: Cyan 🔵
- **Functions**:
  - Uses Tavily search API for real-time deal discovery
  - Targets major Indian e-commerce platforms (Flipkart, Amazon India, etc.)
  - Extracts INR pricing and local product availability
  - Provides fresh, market-relevant deals for Indian consumers

#### 3. **Ensemble Agent** (`agents/ensemble_agent.py`)

- **Role**: Advanced price estimation using multiple models
- **Color**: Yellow 🟡
- **Functions**:
  - Coordinates three different pricing models
  - Uses linear regression to combine predictions optimally
  - Provides robust price estimates through model averaging

#### 4. **Specialist Agent** (`agents/specialist_agent.py`)

- **Role**: Fine-tuned LLM pricing specialist
- **Color**: Red 🔴
- **Functions**:
  - Connects to Modal-hosted fine-tuned Llama 3.1 8B model
  - Provides domain-specific pricing expertise
  - Uses quantized model for efficient inference

#### 5. **Frontier Agent** (`agents/frontier_agent.py`)

- **Role**: RAG-based pricing with similar product context
- **Color**: Blue 🔵
- **Functions**:
  - Performs vector similarity search in ChromaDB
  - Uses OpenAI/DeepSeek with context from 5 similar products
  - Employs sentence transformers for semantic similarity

#### 6. **Random Forest Agent** (`agents/random_forest_agent.py`)

- **Role**: Traditional ML approach to pricing
- **Color**: Magenta 🟣
- **Functions**:
  - Uses scikit-learn Random Forest model
  - Vectorizes product descriptions using sentence transformers
  - Provides baseline ML predictions

#### 7. **Messaging Agent** (`agents/messaging_agent.py`)

- **Role**: Multi-channel notification system
- **Color**: White ⚪
- **Functions**:
  - Sends SMS/WhatsApp alerts via Twilio
  - Optional Pushover push notifications
  - Formatted deal alerts with key metrics

## 🛠️ Technical Stack

### Core Technologies

- **Python 3.8+**: Primary programming language
- **Modal**: Serverless GPU hosting for fine-tuned models
- **ChromaDB**: Vector database for similarity search
- **OpenAI/DeepSeek**: LLM APIs for deal analysis
- **Tavily**: AI-powered search API for real-time Indian deal discovery
- **Twilio**: Communication platform for alerts
- **scikit-learn**: Machine learning models
- **Transformers**: Hugging Face model ecosystem
- **BeautifulSoup**: Web scraping and HTML parsing

### Key Dependencies

```
twilio                 # SMS/WhatsApp notifications
python-dotenv          # Environment variable management
chromadb              # Vector database
scikit-learn          # Machine learning models
numpy                 # Numerical computations
bs4                   # Web scraping
feedparser            # RSS feed parsing
openai                # OpenAI API client
modal                 # Serverless model hosting
sentence-transformers # Text embeddings
tavily-python         # AI search for Indian deals
```

## 📁 Project Structure

```
deals_agents/
├── agents/                    # Agent modules
│   ├── agent.py              # Base agent class with logging
│   ├── planning_agent.py     # Main orchestrator
│   ├── scanner_agent.py      # Deal discovery
│   ├── tavily_scanner_agent.py # Indian deal discovery
│   ├── ensemble_agent.py     # Model coordination
│   ├── specialist_agent.py   # Fine-tuned LLM
│   ├── frontier_agent.py     # RAG-based pricing
│   ├── random_forest_agent.py # ML pricing
│   ├── messaging_agent.py    # Notifications
│   └── deals.py              # Data structures
├── products_vectorstore/      # ChromaDB storage
├── venv/                     # Virtual environment
├── config.py                 # Configuration management
├── pricer_service.py         # Modal service definition
├── deal_agent_framework.py   # Main application entry
├── items.py                  # Product data processing
├── testing.py                # Model evaluation framework
├── memory.json               # Deal history storage
├── requirements.txt          # Python dependencies
├── ensemble_model.pkl        # Trained ensemble weights
├── random_forest_model.pkl   # Trained RF model
├── train.pkl                 # Training dataset
├── test.pkl                  # Testing dataset
└── README.md                 # This file
```

## ⚙️ Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd deals_agents

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file with the following configuration:

```env
# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here

# Optional API Keys
DEEPSEEK_API_KEY=your_deepseek_api_key_here  # Alternative to OpenAI
TAVILY_API_KEY=your_tavily_api_key_here      # For Indian deal discovery (optional)

# Twilio Configuration (for notifications)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_FROM=your_twilio_phone_number
MY_PHONE_NUMBER=your_destination_phone_number
TWILIO_CONTENT_SID=your_whatsapp_template_sid  # Optional

# Pushover Configuration (alternative notifications)
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_app_token
```

### 3. Modal Setup (for Specialist Agent)

```bash
# Install Modal CLI
pip install modal

# Set up Modal authentication
modal token new

# Deploy the pricing service
modal deploy pricer_service.py
```

### 4. Vector Database Initialization

The ChromaDB vector store will be automatically created when you first run the system. Ensure you have the training data (`train.pkl`) in the root directory.

## 🚀 Usage

### Basic Usage

```bash
# Run the complete agent framework
python deal_agent_framework.py
```

### Testing Modal Connection

```bash
# Test the Modal service connection
python test_modal.py
```

### Testing Tavily Scanner

```bash
# Test the Tavily scanner for Indian deals
python test_tavily_scanner.py
```

### Keep Modal Service Warm

```bash
# Prevent Modal cold starts (run in background)
python keep_warm.py
```

### Individual Agent Testing

```python
from agents.planning_agent import PlanningAgent
import chromadb

# Initialize ChromaDB
client = chromadb.PersistentClient(path="products_vectorstore")
collection = client.get_or_create_collection('products')

# Create and run planning agent
planner = PlanningAgent(collection)
opportunities = planner.plan(memory=[])
print(f"Found {len(opportunities)} opportunities")
```

## 📊 Data Flow

1. **Deal Discovery**: Scanner Agent scrapes RSS feeds from DealNews
2. **Content Curation**: OpenAI filters and summarizes promising deals
3. **Price Estimation**: Ensemble Agent coordinates three pricing models:
   - Specialist: Fine-tuned Llama model on Modal
   - Frontier: RAG with similar products from ChromaDB
   - Random Forest: Traditional ML on product vectors
4. **Model Fusion**: Linear regression combines individual predictions
5. **Opportunity Detection**: Deals with >$50 discount are flagged
6. **Alert Generation**: Messaging Agent sends notifications via SMS/WhatsApp

### 📋 **Detailed Execution Analysis**

For a comprehensive walkthrough of the system in action with real logs and step-by-step analysis, see:

**📊 [System Logs Analysis & Execution Flow](SYSTEM_LOGS_EXPLANATION.md)**

This detailed document provides:

- 🚀 Live execution timeline with actual system logs
- 🔍 Phase-by-phase breakdown of agent collaboration
- 💰 Complete deal analysis results from all 5 discovered deals
- ⏱️ Performance metrics and timing analysis
- 🧠 AI model behavior patterns and insights
- 🔬 Technical analysis of the multi-agent coordination

_Perfect for understanding how the 8 AI agents work together to discover and evaluate deals!_

## 🧪 Model Evaluation

The framework includes comprehensive testing utilities:

```python
from testing import Tester
import joblib

# Load test data
test_data = joblib.load('test.pkl')

# Test any pricing function
def my_pricing_function(item):
    return item.price * 1.1  # Example function

# Run evaluation
Tester.test(my_pricing_function, test_data)
```

### Metrics Tracked

- **Average Error**: Mean absolute deviation from true price
- **RMSLE**: Root Mean Squared Logarithmic Error
- **Hit Rate**: Percentage of predictions within 20% of true price
- **Color-coded Results**: Green (good), Orange (okay), Red (poor)

## 🔧 Configuration Options

### Deal Selection Criteria

- **Categories**: Electronics, Computers, Automotive, Smart Home, Home & Garden
- **Quality Threshold**: Minimum description detail and price clarity
- **Discount Threshold**: $50 minimum for notifications
- **Memory System**: Avoids duplicate alerts

### Model Parameters

- **Specialist Model**: Llama 3.1 8B fine-tuned for pricing
- **Vector Model**: all-MiniLM-L6-v2 for embeddings
- **Context Window**: 5 similar products for RAG
- **Token Limits**: 150-160 tokens for product descriptions

### Notification Settings

```python
# In messaging_agent.py
DO_TEXT = True          # Enable SMS/WhatsApp
DO_PUSH = False         # Enable Pushover notifications
USE_WHATSAPP = True     # Use WhatsApp instead of SMS
```

## 📈 Performance Optimization

### Model Optimization

- **Quantization**: 4-bit quantization for Specialist model
- **Caching**: ChromaDB persistence for vector storage
- **Batching**: Bulk processing of deal selections
- **Warm-up**: Keep Modal service active to prevent cold starts

### Monitoring and Logging

- **Color-coded Logging**: Each agent has distinct colors
- **Structured Logging**: Timestamps and agent identification
- **Error Handling**: Graceful fallbacks for API failures
- **Memory Persistence**: JSON-based deal history

## 🛡️ Security and Privacy

### API Key Management

- Environment variable storage with `.env` files
- Graceful degradation when optional keys are missing
- Clear error messages for required configurations

### Data Handling

- Local vector database storage
- No persistent storage of personal data
- RSS feed data only (publicly available deals)

## 🚨 Troubleshooting

### Common Issues

#### Modal Connection Errors

```bash
# Test Modal connectivity
python test_modal.py

# Re-authenticate if needed
modal token new
```

#### Missing Dependencies

```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

#### ChromaDB Issues

```bash
# Clear and reinitialize vector database
rm -rf products_vectorstore/
# Run framework again to rebuild
```

#### API Rate Limits

- OpenAI: Monitor usage in OpenAI dashboard
- Twilio: Check account balance and rate limits
- DeepSeek: Switch to OpenAI if DeepSeek fails

## 🔮 Future Enhancements

### Planned Features

- **Web Dashboard**: Real-time monitoring and deal history
- **Additional Sources**: Amazon, eBay, other deal sites
- **Smart Filtering**: User preference learning
- **Price History**: Tracking deal evolution over time

### Model Improvements

- **Fine-tuning**: Domain-specific model training
- **Ensemble Weights**: Dynamic weight adjustment
- **Category Specialists**: Product-category-specific models
- **Real-time Learning**: Continuous model updates

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support & Contact

For support, please reach out through any of the following channels:

### Developer Contact

- **Name**: Ankit Malik
- **Phone**: +91 8449035579
- **Portfolio**: [https://personal-portfolio-gamma-red.vercel.app/](https://personal-portfolio-gamma-red.vercel.app/)

### Project Support

For technical issues or feature requests:

- Open an issue in the GitHub repository
- Contact the development team through the portfolio website
- Direct message on provided contact number for urgent matters

---

**Note**: This system requires active API keys and proper configuration to function. Please ensure all environment variables are set correctly before running the framework.
