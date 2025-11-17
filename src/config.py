import os

# Make sure to set this in the notebook before running pipelines:
# os.environ["OPENAI_API_KEY"] = "sk-..."
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable.")

# Default chat model
OPENAI_MODEL = "gpt-4o-mini"

# Generation settings
TEMPERATURE = 0.9
MAX_TOKENS = 80

# Length limits
A1_WORD_LIMIT = 40
A2_WORD_LIMIT = 30
