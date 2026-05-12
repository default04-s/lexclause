# LexClause

LexClause is an AI-powered legal assistant prototype designed for rental agreement analysis and legal clause interpretation.

The system combines:
- semantic retrieval,
- legal grounding,
- conversational memory,
- and large language model reasoning

to provide explainable answers based on rental agreement clauses and relevant provisions from the Indian Contract Act, 1872.

---

# Features

- Rental agreement clause retrieval
- Legal provision retrieval
- Conversational legal question answering
- Legal grounding using Indian Contract Act sections
- General User and Professional explanation modes
- Explainable source display
- Semantic vector search using ChromaDB
- Streamlit-based frontend interface

---

# System Architecture

User Query
↓
Embedding Generation
↓
Semantic Retrieval
↓
Clause + Legal Section Retrieval
↓
Prompt Construction
↓
LLM Response Generation
↓
Frontend Display

---

# Tech Stack

- Python
- Streamlit
- ChromaDB
- Sentence Transformers
- Groq API
- HuggingFace Embeddings

---

# Installation

Clone repository:

```bash
git clone https://github.com/default04-s/lexclause.git