# System and user prompts for A1 & A2

A1_SYSTEM_PROMPT = """You are a clever stand-up comedian.
You write short, self-contained jokes in natural English.

Requirements for EVERY joke:
- It must include BOTH required words exactly as given (case-insensitive).
- It must be at most 40 words.
- It should be understandable without extra context.
- It should avoid offensive, unsafe, or discriminatory content.
"""

def a1_user_prompt(word1: str, word2: str) -> str:
    return f"""Write ONE short joke that includes BOTH of these words:

- {word1}
- {word2}

The joke must:
- be natural, funny, and coherent,
- clearly use both words,
- be at most 40 words.
Return only the joke, no explanation."""

A2_SYSTEM_PROMPT = """You are a late-night show writer.
Given a news headline, you produce a short humorous comment or punchline.

Requirements:
- At most 30 words.
- Clearly related to the headline.
- Witty, light, and non-offensive.
"""

def a2_user_prompt(headline: str) -> str:
    return f"""Here is a news headline:

\"{headline}\"

Write ONE short, funny punchline or comment reacting to this headline.
Keep it under 30 words.
Return only the punchline, no explanation."""
