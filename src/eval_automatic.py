import json
from pathlib import Path
from statistics import mean

from .constraints import contains_required_words, within_word_limit, simple_headline_overlap
from .config import A1_WORD_LIMIT, A2_WORD_LIMIT

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

A1_INPUT_FILE = DATA_DIR / "a1_inputs.jsonl"
A1_OUTPUT_FILE = OUTPUT_DIR / "a1_generated.jsonl"

A2_INPUT_FILE = DATA_DIR / "a2_inputs.jsonl"
A2_OUTPUT_FILE = OUTPUT_DIR / "a2_generated.jsonl"


def eval_a1():
    if not A1_INPUT_FILE.exists() or not A1_OUTPUT_FILE.exists():
        print("A1 input or output file missing.")
        return

    total = 0
    word_ok = 0
    len_ok = 0

    with A1_INPUT_FILE.open("r", encoding="utf-8") as fin_inputs, \
         A1_OUTPUT_FILE.open("r", encoding="utf-8") as fin_outputs:

        for in_line, out_line in zip(fin_inputs, fin_outputs):
            inp = json.loads(in_line)
            out = json.loads(out_line)

            joke = out.get("generated_joke", "")
            w1, w2 = inp["word1"], inp["word2"]

            total += 1
            if contains_required_words(joke, [w1, w2]):
                word_ok += 1
            if within_word_limit(joke, A1_WORD_LIMIT):
                len_ok += 1

    print("=== A1 Evaluation ===")
    print(f"Total examples: {total}")
    if total > 0:
        print(f"% jokes containing both words: {word_ok / total * 100:.1f}%")
        print(f"% jokes within length limit:   {len_ok / total * 100:.1f}%")


def eval_a2():
    if not A2_INPUT_FILE.exists() or not A2_OUTPUT_FILE.exists():
        print("A2 input or output file missing.")
        return

    total = 0
    len_ok = 0
    overlaps = []

    with A2_INPUT_FILE.open("r", encoding="utf-8") as fin_inputs, \
         A2_OUTPUT_FILE.open("r", encoding="utf-8") as fin_outputs:

        for in_line, out_line in zip(fin_inputs, fin_outputs):
            inp = json.loads(in_line)
            out = json.loads(out_line)

            headline = inp["headline"]
            joke = out.get("generated_joke", "")

            total += 1
            if within_word_limit(joke, A2_WORD_LIMIT):
                len_ok += 1
            overlaps.append(simple_headline_overlap(headline, joke))

    print("=== A2 Evaluation ===")
    print(f"Total examples: {total}")
    if total > 0:
        print(f"% jokes within length limit: {len_ok / total * 100:.1f}%")
        print(f"Average lexical overlap (Jaccard): {mean(overlaps):.3f}")


def main():
    eval_a1()
    print()
    eval_a2()


if __name__ == "__main__":
    main()
