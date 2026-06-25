# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Course and professor reviews for Long Island University - Brooklyn, sourced from RateMyProfessors. This information is valuable and hard to find through official channels because RateMyProfessors' search and filtering tools make it difficult to quickly compare professors across courses or synthesize patterns (e.g., grading style, workload, attendance policies) without manually reading dozens of individual reviews.
 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate my professor| LIU Brooklyn - search/browse page for all professors | |https://www.ratemyprofessors.com/search/professors/527?q=*
| 2 |RateMyProfessors | Wayne Schnatter (Chemistry) | https://www.ratemyprofessors.com/ShowRatings.jsp?tid=151780|
| 3 | RateMyProfessors| Professor Amara (Mathematics)| https://www.ratemyprofessors.com/professor/951592|
| 4 |RateMyProfessors |Cristal Brooks (Nursing) | https://www.ratemyprofessors.com/professor/2249493|
| 5 |RateMyProfessors | June Lowe (Nursing)| https://www.ratemyprofessors.com/professor/2568856 |
| 6 | RateMyProfessors|Maxwell Kim (Mathematics) | https://www.ratemyprofessors.com/professor/2669403|
| 7 | RateMyProfessors| Morgan Schulz| https://www.ratemyprofessors.com/professor/848498|
| 8 | Niche.com| General LIU student reviews (academics, campus life, professors)|https://www.niche.com/colleges/long-island-university/ |
| 9 | RateMyProfessors| LIU Brooklyn - browse/search all professors page| https://www.ratemyprofessors.com/search/professors/527?q=|
| 10 |Uloop | LIU professor ratings aggregator| https://liu.uloop.com/professors|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 10-150
documents will be stored individually as the reviews tend to be short and to the point

**Overlap:** there will be no overlapping

**Why these choices fit your documents:** they fit because the documents were very small

**Final chunk count:** 51

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**all-MiniLM-L6-v2, via sentence-transformers, running locally with cosine similarity in ChromaDB. I chose it because it's free, requires no API key, runs quickly on a local machine, and is the recommended default for this kind of project — appropriate given the scale of my corpus (51 short chunks).

**Production tradeoff reflection:**If deploying this for real users with cost not a constraint, I would consider a larger embedding model (e.g., OpenAI's text-embedding-3-large or a bigger open-source model) for better accuracy on informal, slang-heavy review text — all-MiniLM-L6-v2 is a relatively small model and may miss nuance in casual student language (e.g., "he's a vibe" or sarcasm). A larger model would also likely have a longer context length, useful if I wanted to combine multiple reviews into longer chunks without losing meaning.

The main tradeoff would be latency and infrastructure: a local model like all-MiniLM-L6-v2 has no network round-trip and no per-query cost, which is ideal for a small project, but an API-hosted model adds latency per query and ongoing cost at scale. For a production system serving many users, I'd weigh whether the accuracy improvement from a larger model justifies the added latency and cost compared to the "good enough" results I got locally with all-MiniLM-L6-v2.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** The model was instructed to answer only using the retrieved review chunks passed as context, and to respond with "I don't have enough information on that" if the answer could not be found in the provided documents. No general knowledge fallback was permitted. The exact instruction given was: "You are an assistant that helps LIU Brooklyn students choose professors. Answer only based on the reviews provided. If the answer is not in the reviews, say: I don't have enough information on that."

**How source attribution is surfaced in the response:**
Each retrieved chunk was labeled with its source filename before being passed to the model, allowing the model to reference which professor the information came from in its response. For example, a chunk from maxwell_kim.txt would be prefixed with "Source: maxwell_kim" so the model could attribute claims to the correct professor.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Is Professor Wayne Schnatter's chemistry class always difficult? | Yes — reviews describe his tests and quizzes as very difficult, with one reviewer recommending students take a different professor instead.|The information is about Professor Wayne Schnatter. According to the reviews, Professor Wayne Schnatter's chemistry class can be difficult, but the level of difficulty may vary depending on the course and the student's perspective |relevant | Accurate
| 2 | What do students say about Professor Amara's grading style? | Reviews describe Amara as a "tough grader" but with "clear grading criteria" and "amazing lectures"; 62% of reviewers said they'd take the class again.| Students consistently describe Professor Amara as a "tough grader". Multiple reviews mention that she takes off points for everything, and one review states that she grades "so harsh".|relevant |accurate | 
| 3 | Would students recommend taking Maxwell Kim for intro to math| Yes — reviews describe him as "the best," with 100% of reviewers saying they'd take him again, and an overall quality rating of 4.9/5| Based on the reviews, the answer is yes, students would highly recommend taking Professor Maxwell Kim for intro to math (MTH100).|relevant |accurate | 
| 4 | Is June Lowe's nursing course (NUR440) considered heavy on reading?| Yes — reviews tag her course as "Get ready to read" and describe it as test-heavy.| The information provided is about Professor June Lowe. According to the reviews, it is mentioned that a textbook is required for the course NUR440, as stated in multiple reviews (Dec 21st, 2025, Dec 29th, 2025, and Jan 9th, 2026). |relevant |accurate |
| 5 | What is the overall student sentiment about LIU Brooklyn's food and facilities? | the school's overall RateMyProfessors rating for "Food" is among the lowest categories (2.6/5), with reviews mentioning issues with the library and broken elevators in the dorms. |I don't have enough information on that. |relevant | acurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** where can i go to buy pizza

**What the system returned:**I don't have enough information on that.

**Root cause (tied to a specific pipeline stage):** there isnt a file containing information about pizza

**What you would change to fix it:** the only change that would be mine is if im trainimg this some more regardimg dininga and maybe letting the model choose where to find pizza places on campus

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The Chunking Strategy section, where I decided each review would be its own chunk, made writing the chunking code straightforward. Since I already knew the goal, I just had to find the pattern that marks where one review ends and the next begins

**One way your implementation diverged from the spec, and why:**My planning.md originally listed 10 sources, including a Niche.com page and a Uloop directory page. While building the pipeline in Milestone 3, I found that neither of these actually contained student reviews, the Niche page was mostly admissions statistics, and the Uloop page was just a list of professor names with no review content. I replaced both with two more individual RateMyProfessors professor pages so every source would actually contribute usable review chunks.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* i used claude to provide me with the code that was needed to clean the data or if there were any error in the terminal i would copy and paste it to claude
- *What it produced:* it gave me step by step answers on what i was supoosed to do with py files and other files
- *What I changed or overrode:* i changed a few .txt files from what they originally where, for example a file that was created for the liu professor rating, i just did the overall rating for a different professor

**Instance 2**

- *What I gave the AI:* i allowed claude to summarize some the milestones however i still ended up reading the milestone
- *What it produced:* it gave a more summarized version of the mileston and also gave me step by step of what i was actually supoosed to do
- *What I changed or overrode:* i didnt necessarily over ride anything for this step.
