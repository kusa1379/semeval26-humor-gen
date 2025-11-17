
SemEval-2026 Humor Generation — Subtasks A1 & A2

Contributors: Kushal Sai Ravindra

This repository contains the complete code and explanation for my final project on the SemEval-2026 Humor Generation Task.
For this project, I focused on the two text-only subtasks for now:

A1: Generate a short joke that must include two specific words

A2: Generate a short humorous comment based on a news headline

I designed this whole system to be:

Simple

Understandable

Easy for anyone to run.

Based entirely on prompt engineering and API calls.

The entire system runs on a CPU and can be executed in Google Colab or on a personal laptop.

1. What These Tasks Are:
   Subtask A1 — Joke with Two Words

The input provides two words like:

"avocado", "spaceship"


My system must generate a short joke (≤ 40 words) that includes both words clearly and in a natural, humorous way.

This is tricky because:

humor is subjective

the model must respect both required words

it still needs to sound natural and funny

In other words:
Can the model connect two random ideas into a joke?

-Subtask A2 — Humor Based on a Headline

The input gives a real or fake news headline like:

"Scientists discover water on Mars again"


My system must write a funny comment (≤ 30 words) that reacts to the headline.
So the goal here is:

understand the headline

generate humor related to it

stay short

remain safe and non-offensive

This is similar to writing a one-liner for a late-night comedy show.

2. How I Designed the System (Very Clear Explanation)

I kept the entire pipeline modular and minimal so the structure is easy to understand.
Here is the main idea:

1. Prompts (prompts.py)

This is the heart of the humor generation.

I wrote two system prompts:

A1 → “You are a stand-up comedian. You must include both words. Keep it short.”

A2 → “You are a late-night show writer. Make a witty comment about the headline.”

Prompts also enforce:

word limits

humor tone

avoiding offensive content

2. Generation (generator_gpt.py)

This file sends requests to the OpenAI API.

To avoid dependency issues in Colab, I didn’t use the openai Python package.
Instead, I used the plain requests library.

Why?

Simple

No version clashes

Works in any environment

This function builds the request → sends it → gets the model's output text.

3. Pipelines (pipeline_a1.py and pipeline_a2.py)

These pipelines do the actual work:

For A1:

Read the input words

Generate a joke

Check:

Are both words present?

Is the joke under 40 words?

If not, try again (up to 5 attempts)

Save the final joke in a JSONL file

For A2:

Read the headline

Generate multiple candidate jokes

Check:

Is the joke ≤ 30 words?

How related is the joke to the headline?

Pick the best candidate based on lexical overlap

Save it

These pipelines guarantee that the outputs follow the task rules.

4. Evaluation (eval_automatic.py)

This part isn’t about “is the joke funny?” (LLMs can’t judge humor well).
Instead, I check:

A1:

% of jokes that contain both required words

% of jokes within 40 words

A2:

% of comments within 30 words

How much the comment overlaps with the headline (simple relevance measure)

This is useful for verifying constraint satisfaction.


Running in Google Colab (recommended)

Clone the repo:

!git clone https://github.com/kusa1379/semeval26-humor-gen.git


Install the dependencies:

!pip install -r semeval26-humor-gen/requirements.txt


Set your API key:

import os
os.environ["OPENAI_API_KEY"] = "sk-..."


Run A1:

%cd semeval26-humor-gen
!python -m src.pipeline_a1


Run A2:

!python -m src.pipeline_a2


Evaluate:

!python -m src.eval_automatic


Outputs appear in the outputs/ folder.

5. Example Results (Easy to Understand)
A1 Example

Input:

{"id": 1, "word1": "algorithm", "word2": "coffee"}


Possible output:

My morning coffee follows a strict algorithm: step one, drink; step two, pretend it helped.


Uses both words + is short + is funny.

A2 Example

Input:

{"id": 1, "headline": "Scientists discover water on Mars again"}


Possible output:

At this point, Mars finds water more consistently than my apartment building does.


Makes a joke while staying relevant.
