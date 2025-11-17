
"""
config.py

This is a Central place to store configuration values and defaults.
If I Need to change the model name or generation settings, I do it here.
"""

import os

#to set the OPENAI_API_KEY in their environment.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable.")

# Iam using gpt-4o-mini OpenAI chat model to use for joke generation. As suggested in the task description.
OPENAI_MODEL = "gpt-4o-mini"

# Generation hyper-parameters: how random the jokes can be, and max length in tokens.
TEMPERATURE = 0.9
MAX_TOKENS = 80

# Hard length limits (in words) for each subtask. These numbers match the constraints we gave in the prompts.
A1_WORD_LIMIT = 40   # max words for two-word jokes
A2_WORD_LIMIT = 30  # max words for headline-based jokes
