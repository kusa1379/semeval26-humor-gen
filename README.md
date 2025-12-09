
SemEval-2026 Humor Generation
Subtasks A1, A2, B1, B2 (EN / ES / ZH + Multimodal GIF Humor)
Contributors: Kushal Sai Ravindra

1. Overview

This repository contains my complete implementation for the SemEval-2026 Humor Generation Task (Task 1). The shared task is about teaching AI systems to generate short, funny, and safe humorous texts under specific constraints.

The project covers all four subtasks:

1. Task A1 (Text-only): Given two words, generate a joke that uses both.

2. Task A2 (Text-only): Given a news-like headline, generate a humorous reaction.

3. Task B1 (Multimodal): Given a GIF URL, generate a humorous caption based only on the GIF.

4. Task B2 (Multimodal): Given a GIF URL + text prompt, generate a humorous caption that relates to both.

Key design choices:

The system is prompt-engineering based, not model training based.

It uses OpenAI GPT models via HTTP API (requests), not the openai Python SDK (to avoid dependency issues in Colab).

Task A is multilingual: English (EN), Spanish (ES), and Chinese (ZH).

Tasks B1/B2 use a vision-capable model (GPT-4o) for GIF understanding.

Everything is designed to run smoothly in Google Colab (CPU for Task A; API handles the heavy lifting).


2. Project Structure

   **data/ — Input Files for All Tasks**

task-a-en-input.tsv / task-a-es-input.tsv / task-a-zh-input.tsv

These files contain the official-style inputs for Task A in English, Spanish, and Chinese.

Each file has two columns:

id – unique identifier for each input instance.

text – either:

exactly two words → interpreted as an A1 instance (two-word joke), or

a longer phrase/headline → interpreted as an A2 instance (headline humor).

The pipeline automatically decides whether each row is A1 or A2 based on the number of tokens.

task-b1-input.tsv

Contains inputs for Task B1 (GIF-only humor).

Columns:

id – unique identifier.

url – URL of a GIF image that the model will use as visual context.


**src/ — Source Code**
prompts.py — All Prompts in One Place

What it contains:

System & user prompts for:

A1 in EN/ES/ZH: jokes using two mandatory words.

A2 in EN/ES/ZH: humorous comments reacting to headlines.

B1: visual-only GIF humor.

B2: GIF + text humor.

Why this file matters:

Humor generation is heavily dependent on prompting.

This file defines:

the “persona” of the model (stand-up comedian, late-night writer, etc.),

the constraints (word limit, safety rules, language of output),

how strict the model must be about including certain words.

Example behaviors:

For A1 English, the system prompt says things like:

“You are a clever stand-up comedian.”

“You must include BOTH required words.”

“Maximum 40 words.”

“Avoid offensive or discriminatory content.”

For A1 Spanish/Chinese:

Same idea, but explicitly asking for output in Spanish or Simplified Chinese, with constraints written in that language.

For B1/B2:

The system prompt says:

“You are a witty comedian who writes short comments about GIFs.”

“Use only what can be seen/inferred from the GIF (for B1), or from both GIF and text (for B2).”

“Keep it under 30 words.”

This file is the control center for the model’s behavior and style.

task-b2-input.tsv


**generator_gpt.py — Text-Only Joke Generator (Task A)**

What it does:

Sends text-only prompts to the OpenAI Chat Completions API using the requests library.

Used by Task A (A1 & A2) in English, Spanish, and Chinese.

Key functions:

_call_gpt(system_prompt, user_prompt, model)

Low-level function:

builds the JSON payload,

sends a POST request,

parses the JSON response,

returns just the generated text.

generate_a1_joke(word1, word2)

Uses the English A1 prompts from prompts.py.

Returns a joke that should include both word1 and word2.

generate_a2_joke(headline)

Uses English A2 prompts.

generate_a1_joke_lang(lang, word1, word2)

Uses language-specific prompts for lang in {en, es, zh}.

generate_a2_joke_lang(lang, headline)

A2 variant for multiple languages.

Why it's written this way:

Using requests instead of the openai SDK avoids:

version conflicts,

proxy keyword errors,

complex SDK updates in Colab.

Separating text-only generation from vision simplifies debugging and makes the code easier to read.


**vision_generator.py — GIF Humor Generator (Tasks B1 & B2)**

What it does:

Handles multimodal requests (text + GIF URL) using a vision-capable GPT-4o model.

Key functions:

_call_gpt_vision(system_prompt, text_prompt, image_url)

Builds a messages payload where the user content includes:

a text chunk (the instructions + optional prompt),

an image_url object pointing to the GIF URL.

Sends it to the API and returns the humorous text.

generate_b1_joke(gif_url)

Uses the B1 system prompt (GIF-only) and a fixed user text like:

“Look at this GIF and write ONE short, funny comment about it.”

generate_b2_joke(gif_url, text_prompt)

Uses the B2 system prompt (GIF + text).

Asks the model to jointly reason about both GIF and given text.

Why separated from generator_gpt.py:

B1/B2 require a different message format (with image_url) and often a different model (gpt-4o).

Keeping vision code separate makes it clearer what is text-only vs. multimodal.

**task_a_tsv_pipeline.py — Master Pipeline for Task A (EN/ES/ZH)**

What it does:

Reads the multilingual input files:

task-a-en-input.tsv

task-a-es-input.tsv

task-a-zh-input.tsv

For each row:

It checks how many tokens the text field has.

If exactly 2 tokens → treat as A1 (two-word joke).

Otherwise → treat as A2 (headline humor).

Calls the appropriate function:

generate_a1_joke_lang(lang, word1, word2)

or generate_a2_joke_lang(lang, headline)

Cleans the output (removes any tabs that might break TSV format).

Writes to:

task-a-en.tsv

task-a-es.tsv

task-a-zh.tsv

Why this file is important:

Automates all of Task A across three languages in a single script.

Ensures everything is output in the exact submission format with id and text.

Centralizes the logic for A1 vs. A2 detection, so you don’t need separate scripts.


**pipeline_b1.py — Pipeline for GIF-Only Humor (Task B1)**

What it does:

Reads data/task-b1-input.tsv:

each item has id and url.

For each row:

calls generate_b1_joke(gif_url) from vision_generator.py.

writes id and the generated humorous text into task-b1.tsv.

Role in the project:

This is the official pipeline that turns raw GIF inputs into submission-ready humor for B1.

Keeps logic for B1 very clean and easy to test (just one TSV in, one TSV out).


**pipeline_b2.py — Pipeline for GIF + Text Humor (Task B2)**

What it does:

Reads data/task-b2-input.tsv:

columns: id, url, prompt.

For each row:

calls generate_b2_joke(gif_url, prompt) from vision_generator.py.

writes id and text into task-b2.tsv.

Why it’s separate from pipeline_b1.py:

B2 combines two inputs (GIF and text) instead of just the GIF.

Having a dedicated file keeps the code for each subtask simple and explicit.


**eval_automatic.py — Simple Automatic Evaluation**

What it does:

For Task A1:

Checks whether both required words still appear in the generated joke.

Counts how many jokes exceed the 40-word limit.

For Task A2:

Checks whether the joke ≤ 30 words.

Computes a simple similarity measure between the headline and the joke (e.g., word overlap).

For Tasks B1/B2:

Checks word length.

Ensures non-empty outputs.

Why this is useful:

The script doesn’t “judge” whether the joke is funny (that’s subjective), but it does verify:

whether your system respects task rules,

how robust the generation is (e.g., constraint satisfaction rate


**config.py — Central Configuration**

Typically stores:

OPENAI_MODEL name for text-only tasks.

TEMPERATURE, MAX_TOKENS, and other generation parameters.

You can tweak this file to experiment without touching all the pipelines.

Why this is good practice:

Easier to tune parameters from one location.

Makes the code cleaner and avoids magic numbers scattered everywhere.


**requirements.txt**

Contains minimal dependencies, for example:

requests for HTTP API calls.

tqdm for progress bars (if used).

Designed to be lightweight and Colab-friendly.


**Outputs — Generated Systems’ Answers**

These files are generated by the pipelines and are in SemEval submission format.

task-a-en.tsv, task-a-es.tsv, task-a-zh.tsv

Columns:

id – copied from the input file.

text – the generated joke/comment for that id.

They are the official outputs for Task A in each language.

task-b1.tsv

Columns:

id – copied from task-b1-input.tsv.

text – humorous caption based only on the GIF.

task-b2.tsv

Columns:

id – copied from task-b2-input.tsv.

text – humorous caption that connects the GIF and the textual prompt.


**3. Tasks Brief Explanations**
**3.1 Task A1 — Two-Word Humor**

Input: two words that may or may not be semantically related.

Model’s job:

Compose a joke that uses both words naturally.

Respect length (≤ 40 words).

Make sense (no random word salad).

This task is a good test of the model’s associative creativity: can it connect “unicorn” and “deadline” or “avocado” and “spaceship” into something that sounds like a joke someone might actually say?


**3.2 Task A2 — Headline-Based Humor**

Input: a news-like headline.

Model’s job:

Understand the scenario.

Imagine how a comedian would react to it.

Generate a short punchline/comment.

This is closer to late-night monologue jokes, where comedians riff on current events. The difficulty is in staying close to the headline content but adding a twist.



**3.3 Task B1 — GIF-Only Humor**

Input: GIF URL.

Model’s job:

“Watch” the GIF using GPT-4o’s vision capabilities.

Detect the basic action or situation (e.g., cat fails a jump, dog spins in a chair).

Write a caption that a human might post on social media.

This checks the ability of the model to combine visual recognition with humorous language.



**3.4 Task B2 — GIF + Text Humor**

Input: GIF URL + short text prompt/headline.

Model’s job:

Understand both the GIF and the text.

Connect them logically in a humorous way.

Keep the answer short and safe.

This is the most complex because the model has to align two different modalities and invent a joke that feels coherent.



**4. How to Run the Entire Project in Google Colab**

**Step 1 — Clone the Repository**

**!git clone https://github.com/kusa1379/semeval26-humor-gen.git**

This command downloads a complete copy of GitHub project into Colab’s temporary filesystem.

After cloning, you will have a folder named semeval26-humor-gen/ that contains: all source code, input data files, the pipelines, and outputs under parent directory.

**Step 2 — Install Dependencies**

**!pip install -r semeval26-humor-gen/requirements.txt**

This reads the requirements.txt file inside your repo. It installs only the minimal packages needed: requests (for API calls) and any other helper libraries.


**Step 3 — Set Your OpenAI API Key**

**import os
  os.environ["OPENAI_API_KEY"] = "sk-..."** (# your API Key)

The humor pipelines need access to GPT-4o / GPT-4o-mini models. The API key is stored in the environment variable OPENAI_API_KEY. All the generator scripts read this variable.


**Step 4 — Move Into the Project Folder**

**%cd semeval26-humor-gen**


**Step 5 — Run Task A (All Languages, A1 + A2)**

**!python -m src.task_a_tsv_pipeline**

Executes the main pipeline for Task A. It automatically: Loads input TSV files for English, Spanish, and Chinese Detects whether each row is A1 or A2 alls the appropriate joke generator (A1 or A2). Generates humor in the correct language and Validates required words, word limits, and safety

Writes three output files:

semeval26-humor-gen/task-a-en.tsv

semeval26-humor-gen/task-a-es.tsv

semeval26-humor-gen/task-a-zh.tsv


**Step 6 — Run Task B1 (GIF-Only Humor)**

**!python -m src.pipeline_b1**

-Reads each row in task-b1-input.tsv.

-Sends the GIF URL to GPT-4o.

-Generates a funny caption based purely on the GIF.

-Saves results to semeval26-humor-gen/task-b1.tsv.


**Step 7 — Run Task B2 (GIF + Text Humor)**

**!python -m src.pipeline_b2**

-Reads GIF + prompt pairs from task-b2-input.tsv.

-Sends both the GIF and the text prompt to GPT-4o.

-Generates a multimodal joke that ties both inputs together.

-Saves results to semeval26-humor-gen/task-b2.tsv.


**After Running Everything**

You will find your final submission files in:

**/content/semeval26-humor-gen/**

