"""
prompts.py

This file contains the system prompts and helper functions that build the
user prompts for each subtask (A1 and A2).

I keep them here so it's easy for me to tweak the style of humor later.
"""
# System prompt for Subtask A1: jokes with two required words.
A1_SYSTEM_PROMPT = """You are a clever stand-up comedian.
You write short, self-contained jokes in English.

Requirements for EVERY joke:(As given in the task description).
- It must include BOTH required words exactly as given (case-insensitive).
- It must be at most 40 words.
- It should be understandable without extra context.
- It should avoid offensive, unsafe, or discriminatory content.
"""

def a1_user_prompt(word1: str, word2: str) -> str:
    """
    Building the user message for A1.
    The model is told exactly which two words must appear in the joke,
    and we remind it of the length and style constraints.
    """
    return f"""Write ONE short joke that includes BOTH of these words:

- {word1}
- {word2}

The joke must:
- be natural, funny
- clearly use both words
- be at most 40 words.
Return the joke."""

# System prompt for Subtask A2: humorous comments based on a news headline.
A2_SYSTEM_PROMPT = """You are a late-night show writer.
Given a news headline, you produce a short humorous comment or punchline.

Requirements:
- At most 30 words.
- Clearly related to the headline.
- Witty, light, and non-offensive.
"""

def a2_user_prompt(headline: str) -> str:
    """
    Building the user message for A2.
    The model receives a headline and is asked to respond with a
    short funny reaction.
    """
    return f"""Here is a news headline:

\"{headline}\"

Write ONE short, funny punchline or comment reacting to this headline.
Keep it under 30 words.
Return only the punchline, no explanation."""
