# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

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

**Reasoning:** i intentionally choose sources that are short, most times people do not have time to read a bag of words, therefore when questions are asked, answers shpould be spitted out in no less that 2/3 sentences. however if any  exceeds the limit then they will be split

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)? all-MiniLM-L6-v2
     How many chunks will you retrieve per query (top-k)?5 chunks retrieved per query
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2

**Top-k:** 5 chunks retrieved per query

**Production tradeoff reflection:**Since each chunk is a single short review representing one student's opinion, retrieving only 1-2 chunks risks surfacing an outlier opinion as if it were consensus. Retrieving the top 5 chunks gives a broader sample of student perspectives on a given professor or topic, allowing the system to identify patterns

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Is Professor Wayne Schnatter's chemistry class always difficult?| Yes — reviews describe his tests and quizzes as very difficult, with one reviewer recommending students take a different professor instead.|
| 2 | What do students say about Professor Amara's grading style? | Reviews describe Amara as a "tough grader" but with "clear grading criteria" and "amazing lectures"; 62% of reviewers said they'd take the class again.|
| 3 | Would students recommend taking Maxwell Kim for intro to math| Yes — reviews describe him as "the best," with 100% of reviewers saying they'd take him again, and an overall quality rating of 4.9/5|
| 4 | Is June Lowe's nursing course (NUR440) considered heavy on reading?| Yes — reviews tag her course as "Get ready to read" and describe it as test-heavy.  |
| 5 |What is the overall student sentiment about LIU Brooklyn's food and facilities? | the school's overall RateMyProfessors rating for "Food" is among the lowest categories (2.6/5), with reviews mentioning issues with the library and broken elevators in the dorms.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.contradictory reviews 

2.missing professors or information on professors who maybe are teaching in a different department

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
     Document ingestion(raw review files)-->chunkin(one review= one chunk)---> Embedding +vector store(all-MiniLM-L6-v2 + chromaDB)---> Retrieval(top-k=5)-->Generation(groq llm API)

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->
     claude will be used for all chucnking, embedding and vector store, generation and retrieval as well as debugging and ill also use gemini if an error occurs

**Milestone 3 — Ingestion and chunking:**
Tool: Claude
- Input: My Documents table (10 RateMyProfessors .txt files) and Chunking Strategy section (one review = one chunk, 10–150 words, no overlap)
- Expected output: A script that loads each .txt file, splits it into individual reviews by detecting review boundaries, and prints the resulting chunks with their source filename
- Verification: Printed 5 chunks and confirmed each one was a single complete student review with no HTML artifacts or fragments


**Milestone 4 — Embedding and retrieval:**
- Tool: Claude
- Input: My Retrieval Approach section (all-MiniLM-L6-v2, top-k=5, ChromaDB with cosine similarity) and the chunk list produced in Milestone 3
- Expected output: A script that embeds each chunk using sentence-transformers, stores the vectors in ChromaDB, and retrieves the top 5 most similar chunks for a given query
- Verification: Ran each of my 5 evaluation questions as queries and confirmed the retrieved chunks were from the correct professor's file

**Milestone 5 — Generation and interface:**
- Tool: Claude
- Input: My system prompt design (answer only from retrieved context, respond with "I don't have enough information on that" if answer not found) and the retrieval output from Milestone 4
- Expected output: A Gradio interface that takes a user question, retrieves the top 5 chunks from ChromaDB, passes them with the system prompt to the Groq llama model, and displays the response
- Verification: Ran all 5 evaluation questions through the full interface and compared responses against expected answers in my Evaluation Plan
