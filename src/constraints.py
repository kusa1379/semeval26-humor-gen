import re
from typing import Iterable


def normalize(text: str) -> str:
    return re.sub(r"\\s+", " ", text.strip()).lower()


def contains_required_words(text: str, words: Iterable[str]) -> bool:
    text_norm = normalize(text)
    return all(w.lower() in text_norm for w in words)


def within_word_limit(text: str, limit: int) -> bool:
    return len(text.split()) <= limit


def simple_headline_overlap(headline: str, joke: str) -> float:
    """
    Very simple lexical overlap measure between headline and joke:
    Jaccard similarity over alphabetic tokens of length > 3.
    """
    def tokenize(s: str):
        return {
            w.lower()
            for w in re.findall(r"[a-zA-Z]+", s)
            if len(w) > 3
        }

    h_set = tokenize(headline)
    j_set = tokenize(joke)

    if not h_set or not j_set:
        return 0.0

    inter = len(h_set & j_set)
    union = len(h_set | j_set)
    return inter / union
