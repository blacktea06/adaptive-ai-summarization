## Project Timeline & Authorship

**Development:** May 2025 – August 2025
**Author:** Paris-Riana Campbell

All core project code was independently developed by me during this period as part of my research work in Human-in-the-Loop Systems (HILS).

# Adaptive AI Summarization

An AI summarization system developed as part of research in **Human-in-the-Loop Systems (HILS)**. The project explores how AI-generated summaries can be adapted to a user's **personality type and cognitive state** to improve human-AI communication.

## Overview

The system generates summaries of technical reports while considering characteristics of the intended reader, including personality type and cognitive state.

The generated summaries are evaluated using both automated metrics and human-centered evaluation methods.

### Workflow

1. Load a technical report.
2. Provide the user's personality type and cognitive state.
3. Generate an AI summary tailored to the user.
4. Measure reading time.
5. Calculate named-entity coverage.
6. Evaluate the summary using ROUGE and BERTScore.
7. Collect human ratings.
8. Conduct a comprehension quiz.
9. Save evaluation results to JSON.

## Evaluation

The project uses several methods to evaluate summary quality:

* **Named-Entity Coverage** — measures how many entities from the original report are preserved.
* **ROUGE** — compares the generated summary with a reference abstract.
* **BERTScore** — evaluates semantic similarity between the generated summary and reference text.
* **Reading Time** — records how long participants take to read the summary.
* **Human Evaluation** — participants rate qualities such as informativeness, coherence, engagement, fluency, understandability, depth, and flexibility.
* **Comprehension Quiz** — evaluates how well participants understood the generated summary.

## Technologies

* Python
* Groq API / OpenAI-compatible API
* spaCy
* BERTScore
* ROUGE
* PyTorch
* JSON

## Research Contribution

The project investigates **human-centered AI communication** by exploring whether AI-generated information can be adapted to characteristics of the person receiving it.

My work included developing the summarization and evaluation pipeline, implementing evaluation metrics, designing the human evaluation process, and developing the overall system architecture.

## Repository Status

This repository contains a **recovered version of the original research implementation**.

Some original project files and experimental outputs were deleted and could not be recovered, including previously generated chapter summaries and historical evaluation results. The recovered code contains the main summarization and evaluation pipeline, but the original experimental results are not included.

## Future Work

* Reproduce the missing experiments and results.
* Test additional personality types and cognitive states.
* Compare personalized and non-personalized summaries.
* Evaluate additional LLMs and metrics.
* Expand human participant testing.
