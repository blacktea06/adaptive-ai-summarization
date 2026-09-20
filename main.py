from openai import OpenAI
from bert_score import score
import torch
from rouge import Rouge
from Human import Human
import os
from pathlib import Path
import json
from datetime import datetime
import spacy
import time

nlp = spacy.load("en_core_web_sm")

client = OpenAI(
    api_key="YOUR_API_KEY_HERE", 
    base_url="https://api.groq.com/openai/v1"
)

def extract_named_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

#NER Coverage Metrics
def compute_named_entity_coverage(original_text, summary_text):
    original_entities = extract_named_entities(original_text)
    summary_entities = extract_named_entities(summary_text)

    original_set = set([ent[0].lower() for ent in original_entities])
    summary_set = set([ent[0].lower() for ent in summary_entities])
    preserved = original_set & summary_set

    coverage_ratio = len(preserved) / len(original_set) if original_set else 0
    coverage_percent = round(coverage_ratio * 100, 2)

    return {
        "original_entities": list(original_set),
        "summary_entities": list(summary_set),
        "preserved_entities": list(preserved),
        "named_entity_coverage_percent": coverage_percent
    }


def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    
def save_results(log_data, filename="results_log.json"):
    # Save results to JSON file
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([log_data], f, indent=4)
    else:
        with open(filename, "r+") as f:
            existing = json.load(f)
            existing.append(log_data)
            f.seek(0)
            json.dump(existing, f, indent=4)


def response(human, report):
    prompt = f"""You are an AI summarization tool.
Take into consideration the human's personality type: {human.personality_type} and their cognitive state: {human.cognitive_state}.
Generate a fluent and grammatical summary of the following report: {report} in 300 words. 

The summary must:

- Accurately include all main points and key details from the source text.
- Use phrasing that closely follows the source text without copying verbatim.
- Preserve important technical terms, names, and numerical data exactly as in the source.
- Avoid adding any information that is not found in the source.
- Be well-structured, coherent, and easy to read.

Please keep in mind the following dimensions as you generate the summary:

1. Semantic Coverage: How many semantic content units from the reference text are covered in the generated text?
2. Factuality: Does the generated text preserve factual statements of source text?
3. Consistency: Is the generated text consistent with the information provided in the source text?
4. Informativeness: How well does the generated text capture the key details of the source text?
5. Coherence: Is the generated text coherent and well-structured?
6. Relevance: Is the generated text relevant to the source text?
7. Fluency: Is the generated text well-written and grammatical?
8. Accuracy: Are there inaccuracies, missing or unfactual statements in the generated text?
9. MQM: How is the overall quality of the generated text?
10. Interest: Is the generated text interesting and engaging?
11. Specific: Is the generated text generic or specific to source text?
12. Correctness: Is the generated text correct or was there a misunderstanding of the source text?
13. Semantically appropriate: Is the generated text semantically appropriate?
14. Understandability: Is the generated text easy to understand?
15. Error Recovery: Is the system able to recover from the errors it makes?
16. Diversity: Is there diversity in the system's responses?
17. Depth: How does the system discuss topics in depth?
18. Likeability: Does the system display a likeable personality?
19. Flexibility: Is the system flexible and adaptive to the user's interests?
20. Inquisitiveness: Is the system inquisitive throughout the conversation?

1. Semantic Coverage
Does it cover all the core content units or main points in the original report?

Your summary mentions many key techniques but might miss some finer points or implications.

2. Informativeness / Depth
Is there enough detail to understand how or why these techniques matter?

Your summary is descriptive but could go deeper into results, impacts, or applications.

3. Engagement / Interest
Does it catch the reader’s attention or motivate curiosity?

The summary is quite factual and neutral; adding significance or context could help.

4. Coherence / Flow
Are the sentences logically connected and easy to follow?

A few sentences feel slightly repetitive or list-like; transitions could be smoother.

5. Specificity
Does it avoid vague/general statements?

Repetition of terms like “entropy rate measures” might reduce specificity; consider variety.

6. Correctness / Accuracy
Any minor misinterpretations or omissions?

Ensure all technical details are exactly right and not oversimplified.

7. Flexibility / Adaptiveness (if tailoring to personality or cognitive state)
Does it adjust tone or focus for the reader’s personality or state?

Your summary is neutral; personalizing style could improve user engagement.

8. Likeability / Style
Does the tone feel approachable or pleasant?

Currently quite technical and neutral; a slightly warmer or clearer style might help.

[Internal Process: Chain of Thought Reasoning Steps] (The chain of thought reasoning steps are not to be provided in the response. )
1. Purpose / Problem: What is the report trying to solve or explain?
2. Approach / Method: How did the authors or operators go about it?
3. Key Events / Findings: What happened? What did they discover or observe?
4. Evaluation / Evidence: What kind of data or validation was provided?
5. Implications / Recommendations: What are the outcomes, takeaways, or next steps?
6. Contextualization: Adjust the tone, focus, or language based on the user’s personality or current state.

ONLY GENERATE THE SUMMARY, DO NOT INCLUDE ANYTHING ELSE IN THE RESPONSE SUCH AS YOUR THOUGHT PROCESS//
OR AN INTRO// BEFORE THE SUMMARY AS WELL AS A CLOSING STATEMENT AFTER THE SUMMARY.// 
MAKE SURE THE SUMMARY IS LESS THAN OR EQUAL TO 300 WORDS. //
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a summarization tool that summarizes the contents of formal reports in a clear and concise way."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=450 #around 300 words maximum  
    )

    return response.choices[0].message.content

def human_evaluation_form(personality_type):
    print("Thanks for participating! Welcome to the Human Evaluation Form!\n")
    print("Please rate the summary you just read on each of the following dimensions. Use a scale from 1 (Very Poor) to 5 (Excellent).There will be a total of 20 questions. Lets begin!)\n")
    informativeness = int(input("1. Informativeness: How useful was the information did that summary provided?: "))
    coherence = int(input("2. Coherence: Did the summary flow logically from beginning to end?: "))
    engagement = int(input("3. Engagement: How engaging or interesting was the summary to read?: "))
    fluency = int(input("4. Fluency: Was the summary grammatically correct and easy to read?: "))
    interest = int(input("5. Interest: Did the content spark your interest or curiosity?: "))
    semantic_appropriateness = int(input("6. Semantic Appropriateness: Was the tone and language appropriate for your cognitive state or personality?: "))
    mqm = int(input("7. MQM: How would you rate the overall quality of the summary?: "))
    understandability = int(input("8. Understandability: Was the summary easy to follow and understand?: "))
    diversity = int(input("9. Diversity: Did the summary show variety in how it presented information?: "))
    depth = int(input("10. Depth: Did the summary go into detail or just skim the surface?: "))
    likeability = int(input("11. Likeability: Did the system's style or tone feel likeable to you?: "))
    flexibility = int(input("12. Flexibility: Did it seem like the summary adapted to your interests?: "))

    return {"personality_type": personality_type,
            "informativeness":informativeness,
            "coherence":coherence,
            "engagement":engagement,
            "fluency":fluency,
            "interest":interest,
            "semantic_appropriateness":semantic_appropriateness,
            "mqm":mqm,
            "understandability":understandability,
            "diversity":diversity,
            "depth":depth,
            "likeability":likeability,
            "flexibility":flexibility,
            "total": informativeness+coherence+engagement+fluency+interest+semantic_appropriateness+mqm+understandability+diversity+depth+likeability+flexibility
            }

def comprehension_quiz():
    print("Welcome to the Comprehension Quiz!\n")
    print(" Answer the following questions based on what you understood from the summary. Your answers help assess clarity and retention.\n")
    main_topic = input("1. What was the main topic of the summary?: \n")
    key_finding = input("2. Name one key finding or result mentioned: \n")
    system = input("3. What system or technology was discussed?: \n")
    enviornment = input("4. What was the environment or context of the summary? (e.g., Moon, Mars, Earth): \n")
    impact = input("5. What was the impact of the system or technology?: \n")
    trade_off = input("6. Was there a trade-off or comparison made? If so, what?: \n")
    explanation = input("7. Did the summary explain how the system works? If so, how did you interpret it in your own words?: \n")
    metrics = input("8. Were any performance metrics or numbers included? If so, what did they represent?: \n")
    interest = input("9. What was the most suprising or intesting thing you learned from the summary?: \n")
    confidence = input("10. Would you feel confident explaining this summary to someone else? Why or why not?: \n")
    
    return {"main_topic":main_topic,
            "key_finding":key_finding,
            "system":system,
            "enviornment":enviornment, 
            "impact":impact,
            "trade_off":trade_off, 
            "explanation":explanation, 
            "metrics":metrics, 
            "interest":interest, 
            "confidence":confidence}

def word_count(text):
    return len(text.split())

def main(human):
    chunk_path = r"Summary_AI\NASA-TP-2525_Chunk3.txt"
    abstract_path = r"Summary_AI\NASA-TP-2525_Abstract.txt"


    chunk_text = load_text(chunk_path)
    abstract_text = load_text(abstract_path)

    summary = response(human, chunk_text)
    print(summary)

    #Reading Time
    start_time = time.time()

    input("Press Enter after you finish reading the summary...")

    end_time = time.time()

    reading_time_seconds = round(end_time - start_time, 2)
    print(f"Human reading time: {reading_time_seconds} seconds")

    #NER
    named_entities = extract_named_entities(chunk_text)
    summary_entities = extract_named_entities(summary)
    named_entity_metrics = compute_named_entity_coverage(chunk_text, summary)


    print("\n--- Named Entities in Original Report ---")
    print(named_entities)

    print("\n--- Named Entities in Summary ---")
    print(summary_entities)

    print("\n--- Named Entity Coverage Metrics ---")
    print(named_entity_metrics)


    # ROUGE scoring
    rouge = Rouge()
    rouge_scores = rouge.get_scores(summary, abstract_text)[0]

    # BERTScore
    P, R, F1 = score([summary], [abstract_text], lang='en', model_type='bert-base-uncased')
    bert_score = {
        "precision": P[0].item(),
        "recall": R[0].item(),
        "f1": F1[0].item()
    }

    #Human Evaluation
    human_score = human_evaluation_form(human.personality_type)
    human_comprehension = comprehension_quiz()

    # Show results
    print("\n--- Evaluation Metrics ---\n")
    print("ROUGE Scores:", rouge_scores)
    print("BERTScore:", bert_score)

    log_data = {
        "name": human.name,
        "timestamp": datetime.now().isoformat(),
        "chunk_file": chunk_path,
        "abstract_file": abstract_path,
        "summary": summary,
        "named_entities_report": named_entities,
        "named_entities_summary": summary_entities,
        "named_entity_metrics": named_entity_metrics,
        "personality": human.personality_type,
        "cognitive_state": human.cognitive_state,
        "rouge_scores": rouge_scores,
        "bert_score": bert_score,
        "human_ratings": human_score,
        "comprehension_answers": human_comprehension,
        "word count": word_count(summary),
        "reading_time_seconds": reading_time_seconds,
    }

    save_results(log_data)

human = Human("Hamid","ENTP","fatigued")

main(human)




