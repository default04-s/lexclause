# LexClause

LexClause is an AI-powered legal assistant for contract analysis that combines semantic retrieval, legal grounding, clause reranking, and large language model reasoning to answer questions about contracts.

The system currently supports:

- Employment Agreements
- Residential Rental Agreements
- Mutual Non-Disclosure Agreements (NDAs)
- Service Agreements

Responses are generated using relevant contract clauses together with applicable provisions of the Indian Contract Act, 1872.

---

# Features

- Multi-contract support
- Semantic contract clause retrieval using ChromaDB
- Legal provision retrieval from the Indian Contract Act, 1872
- CrossEncoder-based clause reranking
- Dual-source Retrieval-Augmented Generation (RAG)
- Conversational legal question answering
- Legal grounding using relevant statutory provisions
- General User and Professional explanation modes
- Explainable source display
- Streamlit-based frontend interface

---

# System Architecture

User Query

↓

Embedding Generation

↓

Contract Collection Selection

↓

Semantic Retrieval (Top 5)

↓

CrossEncoder Clause Reranking

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
- CrossEncoder (MS MARCO MiniLM)
- Groq API (Llama 3.1)
- Hugging Face Embeddings

---

# Installation

Clone the repository:

```bash
git clone https://github.com/default04-s/lexclause.git
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run frontend.py
```

---

# Project Structure

```
data/
    employment_contract.txt
    rental_contract.txt
    nda_contract.txt
    service_contract.txt
    legal_text.txt

utils/
    extractor.py
    cleaner.py
    segmenter.py
    legal_segmenter.py
    embedder.py
    vectordb.py
    reranker.py
    prompt_builder.py
    llm.py

frontend.py
ingest.py
legal_ingest.py
```

---

# Supported Contract Types

- Employment Agreement
- Residential Rental Agreement
- Mutual Non-Disclosure Agreement (NDA)
- Service Agreement

---

# Legal Knowledge Base

The legal knowledge base contains selected provisions of the Indian Contract Act, 1872 relevant to the supported contract types. These provisions are segmented, embedded, stored separately in ChromaDB, and retrieved alongside contract clauses to provide legally grounded responses.