"""
generator_gpt.py

Text-only generator for Task A (A1 + A2), including multilingual support.
Uses the OpenAI Chat Completions API via the 'requests' library.
"""

import os
import requests

from .config import OPENAI_MODEL, TEMPERATURE, MAX_TOKENS
from .prompts import (
    A1_SYSTEM_PROMPT,
    A2_SYSTEM_PROMPT,
    a1_user_prompt,
    a2_user_prompt,
    get_a1_prompts,
    get_a2_prompts,
)

API_KEY = os.getenv("OPENAI_API_KEY")
if API_KEY is None:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

API_URL = "https://api.openai.com/v1/chat/completions"


def _call_gpt(system_prompt: str, user_prompt: str, model: str = None) -> str:
    if model is None:
        model = OPENAI_MODEL

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }

    resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


# ---------- Original English-only helpers (for your JSONL experiments) ----------

def generate_a1_joke(word1: str, word2: str) -> str:
    return _call_gpt(A1_SYSTEM_PROMPT, a1_user_prompt(word1, word2))


def generate_a2_joke(headline: str) -> str:
    return _call_gpt(A2_SYSTEM_PROMPT, a2_user_prompt(headline))


# ---------- Multilingual helpers for official Task A TSV pipelines ----------

def generate_a1_joke_lang(lang: str, word1: str, word2: str) -> str:
    system_prompt, user_prompt = get_a1_prompts(lang, word1, word2)
    return _call_gpt(system_prompt, user_prompt)


def generate_a2_joke_lang(lang: str, headline: str) -> str:
    system_prompt, user_prompt = get_a2_prompts(lang, headline)
    return _call_gpt(system_prompt, user_prompt)