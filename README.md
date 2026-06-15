# ⚡ DataPulse AI

A unique, all-in-one data processing system that combines:
- **Data ingestion & cleaning** (CSV/Excel/JSON)
- **AI-powered insights generation** (with optional OpenAI integration)
- **ESG (Environmental, Social, Governance) analysis**
- **Cybersecurity risk scanning**
- **Beautiful visualizations**
- **Automated workflow orchestration**
- **Web-based dashboard** for easy use

## ✨ What makes this unique?

This engine doesn't just process data—it adds intelligent, multi-dimensional analysis that's typically siloed across different tools. By combining:
- Data quality & cleaning
- AI-powered business insights
- ESG performance metrics
- Cybersecurity risk assessments
- Professional visualizations

In one fully autonomous pipeline, it delivers a holistic view of your data assets with zero manual effort!

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Web Dashboard!
```bash
python app.py
```
Then open your browser and go to: **(https://datapulse-ai-7006.onrender.com/)**

### 3. Or use the command line
```bash
# Quick demo
python run_demo.py

# Process your own files
python main.py
```

## 🎯 Features

### 📊 Data Processing
- Ingests CSV, Excel, and JSON files
- Cleans & normalizes data automatically
- Handles missing values
- Generates statistical analysis

### 🤖 AI Insights
- **Demo mode**: Built-in intelligent analysis
- **OpenAI mode**: Real LLM-powered insights (just add your API key)
- Generates key findings, recommendations, and business impact

### 🌱 ESG Analysis
- Scans for environmental, social, and governance indicators
- Calculates ESG scores
- Provides improvement recommendations

### 🔒 Cybersecurity Scanning
- Detects PII, credit cards, IP addresses, API keys
- Risk level assessment (Low → Critical)
- Security best practice recommendations

### 📈 Visualizations
- Revenue & expense trends
- Departmental performance
- Distribution analysis
- Correlation heatmaps
- And more!

### 🖥️ Web Dashboard
- Drag-and-drop file upload
- Beautiful, responsive interface (Tailwind CSS)
- View all results in one place
- Download cleaned data & charts
- History of previous runs

## 🔑 OpenAI Integration (Optional)

To use real AI insights instead of demo mode:

1. Copy the example env file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key
   ```

That's it! The engine will automatically use the OpenAI API when available, falling back to demo mode if not!

## 📁 Project Structure

```
autonomous-workflow-engine/
├── config/                   # Configuration files
├── input_data/               # Drop your data files here
├── output_demo/              # Generated output directories
├── templates/                # Web dashboard templates
├── src/
│   ├── core/                # Data ingestion & processing
│   ├── ai_insights/         # AI-powered analysis
│   ├── esg/                 # ESG metrics analyzer
│   ├── cybersecurity/       # Security risk scanner
│   ├── visualizations/      # Chart & graph generation
│   └── workflow/            # End-to-end orchestration
├── requirements.txt
├── .env.example             # Example environment variables
├── run_demo.py              # Quick demo script
├── main.py                  # CLI entry point
└── app.py                   # Web dashboard (Flask)
```

## 📦 Output

Each run creates a unique timestamped directory in `output_demo/` containing:
- `*_cleaned.csv` - Processed & cleaned data
- `*_analysis.json` - Statistical analysis
- `ai_insights.json` - AI-generated business insights
- `esg_analysis.json` - ESG performance metrics
- `cybersecurity_risk_report.json` - Security risk assessment
- `EXECUTIVE_SUMMARY.json` - High-level overview
- `charts/` - Directory with all generated visualizations!

## 🛠️ Tech Stack

- **Python** - Core language
- **Flask** - Web dashboard
- **Pandas** - Data processing
- **Matplotlib/Seaborn** - Visualizations
- **OpenAI API** - Optional AI insights
- **Tailwind CSS** - Beautiful UI


## Components

### 1. Data Processor (`src/core/`)
- Supports CSV, Excel, JSON files
- Cleans & normalizes data automatically
- Handles missing values

### 2. AI Insights (`src/ai_insights/`)
- Demo mode with intelligent analysis
- Extendable for real LLM integration
- Generates business recommendations

### 3. ESG Analyzer (`src/esg/`)
- Scans for ESG-related keywords
- Calculates environmental, social, governance scores
- Provides improvement recommendations

### 4. Security Scanner (`src/cybersecurity/`)
- Detects PII, credit cards, API keys
- Risk level assessment
- Security recommendations

### 5. Orchestrator (`src/workflow/`)
- End-to-end workflow automation
- Coordinates all components
- Generates structured output directories
