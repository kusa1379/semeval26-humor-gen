import json
from pathlib import Path
from tqdm import tqdm

from .generator_gpt import generate_a2_joke
from .constraints import within_word_limit, simple_headline_overlap
from .config import A2_WORD_LIMIT

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

A2_INPUT_FILE = DATA_DIR / "a2_inputs.jsonl"
A2_OUTPUT_FILE = OUTPUT_DIR / "a2_generated.jsonl"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with A2_INPUT_FILE.open("r", encoding="utf-8") as fin, \
         A2_OUTPUT_FILE.open("w", encoding="utf-8") as fout:

        for line in tqdm(fin, desc="Generating A2 jokes"):
            sample = json.loads(line)
            headline = sample["headline"]

            best_joke = None
            best_overlap = -1.0
            last_candidate = ""

            for _ in range(5):
                candidate = generate_a2_joke(headline)
                last_candidate = candidate
                if not within_word_limit(candidate, A2_WORD_LIMIT):
                    continue
                overlap = simple_headline_overlap(headline, candidate)
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_joke = candidate

            if best_joke is None:
                best_joke = last_candidate

            sample["generated_joke"] = best_joke
            sample["headline_overlap"] = float(best_overlap)
            fout.write(json.dumps(sample, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
