"""
vision_generator.py

Multimodal (image/GIF) generator for Task B1 and B2.
We send the GIF URL directly to the OpenAI API as an image_url.
"""

import os
import requests

from .prompts import (
    B1_SYSTEM_PROMPT,
    b1_user_prompt,
    B2_SYSTEM_PROMPT,
    b2_user_prompt,
)

API_KEY = os.getenv("OPENAI_API_KEY")
if API_KEY is None:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

API_URL = "https://api.openai.com/v1/chat/completions"

# Use a vision-capable model.
VISION_MODEL = "gpt-4o"


def _call_gpt_vision(system_prompt: str, text_prompt: str, image_url: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": VISION_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text_prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            },
        ],
        "temperature": 0.9,
        "max_tokens": 80,
    }

    resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


def generate_b1_joke(gif_url: str) -> str:
    """Task B1: Single GIF → humorous comment (English)."""
    return _call_gpt_vision(B1_SYSTEM_PROMPT, b1_user_prompt(), gif_url)


def generate_b2_joke(gif_url: str, text_prompt: str) -> str:
    """Task B2: GIF + text prompt → humorous comment."""
    return _call_gpt_vision(B2_SYSTEM_PROMPT, b2_user_prompt(text_prompt), gif_url)
