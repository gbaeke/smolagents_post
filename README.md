# Smolagents and Azure OpenAI tutorial

## Setup

1. Clone the repository and navigate into the project directory
2. Install dependencies with: `pip install -r requirements.txt`
3. Create a `.env` file with your API keys:
   - OPENAI_API_KEY=your_openai_key
   - BING_SUBSCRIPTION_KEY=your_bing_key
4. For telemetry, run `python -m phoenix.server.main serve` before running the agent
   - See https://huggingface.co/docs/smolagents/tutorials/inspect_runs for more information

## Usage

Run the assistant by providing your question as a command-line argument:

```
python app.py "your question in quotes"
```

Example commands:
- `python app.py "What is DeepSeek R1?"`
- `python app.py "Search for Python API tutorials"`

## How it Works

The assistant uses three main components:

1. **CodeAgent**: Orchestrates the tools and processes natural language commands
2. **Tools**:
   
3. **LLM**: Uses GPT-4o to understand commands and generate responses

## Requirements

- Python 3.8+
- Azure OpenAI API key and endpoint
- Bing API key