"""
generator_gpt.py

This file talks to the OpenAI API using the HTTP "requests" library.
We avoid using the `openai` Python package entirely to prevent
version conflicts in Colab or local machines.
"""

import os
import requests

from .config import OPENAI_MODEL, TEMPERATURE, MAX_TOKENS
from .prompts import (
    A1_SYSTEM_PROMPT,
    A2_SYSTEM_PROMPT,
    a1_user_prompt,
    a2_user_prompt,
)

# API Key must be set in environment variable:
#   export OPENAI_API_KEY="sk-..."
API_KEY = os.getenv("OPENAI_API_KEY")
if API_KEY is None:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

# OpenAI Chat Completion endpoint
API_URL = "https://api.openai.com/v1/chat/completions"


def _call_gpt(system_prompt: str, user_prompt: str) -> str:
    """
    Low-level helper function that sends a chat completion request.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }

    # Make the HTTP request
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    return data["choices"][0]["message"]["content"].strip()


def generate_a1_joke(word1: str, word2: str) -> str:
    """Generate a Subtask A1 joke based on two required words."""
    return _call_gpt(
        A1_SYSTEM_PROMPT,
        a1_user_prompt(word1, word2),
    )


def generate_a2_joke(headline: str) -> str:
    """Generate a Subtask A2 humorous punchline based on a news headline."""
    return _call_gpt(
        A2_SYSTEM_PROMPT,
        a2_user_prompt(headline),
    )
