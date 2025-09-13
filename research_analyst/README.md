# AI Research Analyst - CrewAI Project

An intelligent multi-agent system that generates comprehensive AI use case reports for any company using CrewAI framework. The system analyzes company websites, researches industry applications, and produces detailed reports with 15+ prioritized AI use cases.

## Features

- **Multi-Agent System**: Two specialized AI agents (Researcher & Reporting Analyst)
- **Web Research**: Automated company website analysis and industry research
- **Comprehensive Reports**: Generates detailed markdown reports with business impact analysis
- **Streamlit Interface**: User-friendly web interface for dynamic input and real-time monitoring
- **Multiple LLM Support**: Compatible with Gemini, Groq, and OpenRouter models
- **Real-time Progress**: Live verbose output display during analysis
- **Dynamic File Naming**: Automatic timestamped report generation

## Project Structure

```
research_analyst/
├── src/research_analyst/
│   ├── config/
│   │   ├── agents.yaml          # Agent configurations
│   │   └── tasks.yaml           # Task definitions
│   ├── tools/
│   │   └── custom_tool.py       # Custom tools (if needed)
│   ├── crew.py                  # Main crew orchestration
│   └── main.py                  # CLI entry point
├── Reports/                     # Generated reports directory
├── streamlit_app.py            # Streamlit web interface
├── .env                        # Environment variables
├── pyproject.toml              # Project dependencies
└── README.md                   # This file
```

## Installation

### Prerequisites
- Python >=3.10 <3.14
- UV package manager (recommended) or pip

### Setup

1. **Clone and navigate to the project:**
```bash
cd research_analyst
```

2. **Install dependencies:**
```bash
# Using UV (recommended)
crewai install

# Or using pip
pip install -r requirements.txt
```

3. **Install Streamlit dependencies:**
```bash
pip install -r streamlit_requirements.txt
```

### Environment Configuration

Create/update your `.env` file with the following variables:

```env
# Model Configuration
MODEL=gemini/gemini-2.5-flash
THINKING=openrouter/qwen/qwen-2.5-7b-instruct:free

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

**Required API Keys:**
- **Gemini API**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OpenRouter API**: Get from [OpenRouter](https://openrouter.ai/keys)
- **Serper API**: Get from [Serper](https://serper.dev/api-key)

## Usage

### Option 1: Streamlit Web Interface (Recommended)

1. **Launch the Streamlit app:**
```bash
streamlit run streamlit_app.py
```

2. **Use the interface:**
   - Enter company name and website URL
   - Click "Generate Report"
   - Monitor real-time progress and verbose output
   - Download the generated report

**Features:**
- Dynamic input fields for company name and website
- Real-time progress tracking with status updates
- Live verbose output display (ANSI-cleaned)
- Automatic file naming: `CompanyName_YYYY-MM-DD_HH-MM-SS.md`
- Instant report download and preview
- Error handling with separate error display area

### Option 2: Command Line Interface

```bash
crewai run
```

*Note: CLI uses hardcoded inputs in `main.py` - modify as needed*

## Agents & Tasks

### Agents

1. **Senior Researcher**
   - Role: Data science, ML and AI specialist
   - Tools: SerperDevTool, ScrapeWebsiteTool
   - Goal: Uncover AI use cases and workflow automations

2. **Reporting Analyst**
   - Role: Technical communication specialist
   - Goal: Create detailed reports for non-technical audiences

### Tasks

1. **Research Task**
   - Analyze company website and products
   - Research industry AI applications
   - Identify 15+ potential AI use cases

2. **Reporting Task**
   - Generate comprehensive markdown report
   - Include business context and technical implementation
   - Provide quantifiable outcomes and success metrics

## Report Structure

Generated reports include:

1. **Executive Summary** - High-level overview
2. **15 Prioritized AI Use Cases** with:
   - Specific use case and business context
   - Technical implementation approach
   - Quantifiable expected outcomes and success metrics
3. **Supporting Evidence** - Validation and analysis

## Configuration

### Model Selection

Supported LLM providers:

- **Gemini**: `gemini/gemini-2.5-flash`
- **OpenRouter**: Various models including:
  - `openrouter/qwen/qwen-2.5-7b-instruct:free`
  - `openrouter/meta-llama/llama-3.1-8b-instruct:free`
  - `openrouter/google/gemini-flash-1.5:free`

### Embeddings

Uses HuggingFace embeddings to avoid OpenAI dependency:
```yaml
embedder:
  provider: "huggingface"
  config:
    model: 'sentence-transformers/all-MiniLM-L6-v2'
```

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**: Ensure embedder configuration is set to HuggingFace
2. **Rate Limiting**: Switch to different OpenRouter models if rate-limited
3. **Tool Calling Issues**: Some models may not support all tool features
4. **Verbose Output Not Showing**: Check ANSI code stripping in StreamCapture class

### Model Compatibility

- **Gemini**: Full feature support including tools and reasoning
- **OpenRouter**: Varies by model - test different models if issues occur
- **Groq**: Limited tool calling support depending on model

## File Output

- **Location**: `research_analyst/Reports/`
- **Naming**: `CompanyName_YYYY-MM-DD_HH-MM-SS.md`
- **Format**: Markdown with structured sections
- **Size**: Typically 15-25KB depending on company complexity

## Performance

- **Analysis Time**: 5-10 minutes depending on company complexity
- **Rate Limits**: Configured with conservative RPM limits
- **Caching**: Enabled for improved performance on repeated runs
