"""
pipeline_b2.py

Generate official TSV submission for Task B2 (GIF + text prompt humor).

Expected input:
- data/task-b2-input.tsv

Format:
- header line
- columns: id<TAB>url<TAB>prompt

Output:
- task-b2.tsv with columns: id<TAB>text
"""

from pathlib import Path
from .vision_generator import generate_b2_joke

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "task-b2-input.tsv"
OUTPUT_FILE = BASE_DIR / "task-b2.tsv"


def main():
    if not INPUT_FILE.exists():
        print(f"[WARN] Input file not found: {INPUT_FILE}")
        return

    with INPUT_FILE.open("r", encoding="utf-8") as fin, \
         OUTPUT_FILE.open("w", encoding="utf-8") as fout:

        fout.write("id\ttext\n")
        header = fin.readline()  # skip header

        for line in fin:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue

            sample_id = parts[0]
            gif_url = parts[1].strip()
            text_prompt = parts[2].strip()

            joke = generate_b2_joke(gif_url, text_prompt)
            joke_clean = joke.replace("\t", " ")
            fout.write(f"{sample_id}\t{joke_clean}\n")


if __name__ == "__main__":
    main()
