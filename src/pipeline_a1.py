"""
pipeline_a1.py

End-to-end pipeline for Subtask A1 (two-word constrained jokes).

Steps:
1. Read inputs from data/a1_inputs.jsonl
2. For each line, call the generator to produce a joke
3. Check that the joke satisfies:
     - contains both required words
     - respects word limit
   (we allow up to 5 attempts)
4. Save the final joke in outputs/a1_generated.jsonl

The script is written so it works both in Colab and on a local machine.
"""
import json
from pathlib import Path
from tqdm import tqdm

from .generator_gpt import generate_a1_joke
from .constraints import contains_required_words, within_word_limit
from .config import A1_WORD_LIMIT

# Base dir = project root (one level above src/)
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

A1_INPUT_FILE = DATA_DIR / "a1_inputs.jsonl"
A1_OUTPUT_FILE = OUTPUT_DIR / "a1_generated.jsonl"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with A1_INPUT_FILE.open("r", encoding="utf-8") as fin, \
         A1_OUTPUT_FILE.open("w", encoding="utf-8") as fout:

        for line in tqdm(fin, desc="Generating A1 jokes"):
            sample = json.loads(line)
            w1, w2 = sample["word1"], sample["word2"]

            joke = None
            candidate = ""
            for _ in range(5):  # up to 5 attempts
                candidate = generate_a1_joke(w1, w2)
                if contains_required_words(candidate, [w1, w2]) and within_word_limit(candidate, A1_WORD_LIMIT):
                    joke = candidate
                    break
            if joke is None:
                joke = candidate  # fallback

            sample["generated_joke"] = joke
            fout.write(json.dumps(sample, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
