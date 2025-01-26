from smolagents import CodeAgent, LiteLLMModel
import os
import sys
from dotenv import load_dotenv
from tools import bing_search

# instrumentation
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

endpoint = "http://0.0.0.0:6006/v1/traces"
trace_provider = TracerProvider()
trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)


def print_usage():
    print("\nUsage: python search.py \"your question in quotes\"")
    print("\nExample:")
    print("  python search.py \"Find the cheapest laptop\"")
    print("  python search.py \"Find a Python tutorial to write a FastAPI API\"")
    sys.exit(1)

def main():
    # Check if a question was provided
    if len(sys.argv) != 2:
        print("\nError: Please provide a question as a command-line argument.")
        print_usage()

    # Get the question from command line
    question = sys.argv[1]

    # Load environment variables from .env file
    load_dotenv()

    # Check for required environment variables
    required_vars = ["AZURE_OPENAI_API_KEY", "BING_SUBSCRIPTION_KEY", "AZURE_API_BASE", "AZURE_MODEL"]
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            print(f"\nError: {var} not found in .env file")
            missing_vars.append(var)
    if missing_vars:
        sys.exit(1)

    # get keys from .env
    azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_api_base = os.getenv("AZURE_API_BASE")
    azure_model = os.getenv("AZURE_MODEL")
    bing_subscription_key = os.getenv("BING_SUBSCRIPTION_KEY")
    # refer to Azure model as azure/NAME_OF_YOUR_DEPLOYED_MODEL
    model = LiteLLMModel(model_id=f"azure/{azure_model}", api_key=azure_openai_api_key, api_base=azure_api_base, max_tokens=4096)

    # add bing search tool
    tools = [
        bing_search.BingSearchTool(api_key=bing_subscription_key)
    ]
    
    agent = CodeAgent(
        model=model,
        max_steps=10,
        verbosity_level=2,
        tools=tools,
        additional_authorized_imports=["requests", "bs4"]
    )

    extra_instructions="""
        Answer in plain text. Do not use markdown or JSON.
    """

    result = agent.run(question + " " + extra_instructions)

if __name__ == "__main__":
    main()
    