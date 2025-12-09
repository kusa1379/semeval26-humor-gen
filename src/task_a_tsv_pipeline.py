"""
task_a_tsv_pipeline.py

Generate official TSV submissions for Task A in English, Spanish, and Chinese.

Expected input files:
- data/task-a-en-input.tsv
- data/task-a-es-input.tsv
- data/task-a-zh-input.tsv

Each input TSV:
- header line
- columns: id<TAB>text
  where text is either:
    - exactly two tokens -> A1 (two-word joke)
    - otherwise          -> A2 (headline joke)

Outputs (in repo root, as required by SemEval):
- task-a-en.tsv
- task-a-es.tsv
- task-a-zh.tsv
"""

from pathlib import Path
from .generator_gpt import generate_a1_joke_lang, generate_a2_joke_lang

BASE_DIR = Path(__file__).resolve().parents[1]

LANG_CONFIG = {
    "en": {
        "input": BASE_DIR / "data" / "task-a-en-input.tsv",
        "output": BASE_DIR / "task-a-en.tsv",
    },
    "es": {
        "input": BASE_DIR / "data" / "task-a-es-input.tsv",
        "output": BASE_DIR / "task-a-es.tsv",
    },
    "zh": {
        "input": BASE_DIR / "data" / "task-a-zh-input.tsv",
        "output": BASE_DIR / "task-a-zh.tsv",
    },
}


def process_language(lang: str, input_path: Path, output_path: Path):
    print(f"Processing Task A for language: {lang}  ({input_path.name} -> {output_path.name})")
    if not input_path.exists():
        print(f"  [WARN] Input file not found: {input_path}")
        return

    with input_path.open("r", encoding="utf-8") as fin, \
         output_path.open("w", encoding="utf-8") as fout:

        # submission header
        fout.write("id\ttext\n")

        # skip input header
        header = fin.readline()

        for line in fin:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue

            sample_id = parts[0]
            text = parts[1].strip()

            tokens = text.split()
            # Heuristic: exactly two tokens -> A1; otherwise -> A2.
            if len(tokens) == 2:
                word1, word2 = tokens
                joke = generate_a1_joke_lang(lang, word1, word2)
            else:
                joke = generate_a2_joke_lang(lang, text)

            joke_clean = joke.replace("\t", " ")
            fout.write(f"{sample_id}\t{joke_clean}\n")


def main():
    for lang, cfg in LANG_CONFIG.items():
        process_language(lang, cfg["input"], cfg["output"])


if __name__ == "__main__":
    main()
