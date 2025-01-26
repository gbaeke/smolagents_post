from smolagents import CodeAgent, LiteLLMModel
import os
import sys
from dotenv import load_dotenv

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
    print("\nUsage: python app.py \"your question in quotes\"")
    print("\nExample:")
    print("  python app.py \"Find the cheapest laptop\"")
    print("  python app.py \"Find a Python tutorial to write a FastAPI API\"")
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
    if not os.getenv("AZURE_OPENAI_API_KEY"):
        print("\nError: OPENAI_API_KEY not found in .env file")
        sys.exit(1)
    if not os.getenv("BING_SUBSCRIPTION_KEY"):
        print("\nError: BING_SUBSCRIPTION_KEY not found in .env file")
        sys.exit(1)
    if not os.getenv("AZURE_API_BASE"):
        print("\nError: AZURE_API_BASE not found in .env file")
        sys.exit(1)

    # get keys from .env
    azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_api_base = os.getenv("AZURE_API_BASE")

    model = LiteLLMModel(model_id="azure/gpt-4o-global", api_key=azure_openai_api_key, api_base=azure_api_base, max_tokens=4096)
    
    agent = CodeAgent(
        model=model,
        max_steps=10,
        verbosity_level=2,
        tools=[]
    )

    extra_instructions="""
        Answer in plain text. Do not use markdown or JSON.
    """

    result = agent.run(question + " " + extra_instructions)

if __name__ == "__main__":
    main()
    