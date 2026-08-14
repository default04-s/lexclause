import streamlit as st

from utils.reranker import rerank_results
from utils.embedder import generate_query_embedding

from utils.vectordb import (
    search_clauses,
    search_legal_sections,
    collection_has_data
)

from ingest import ingest_contracts
from legal_ingest import ingest_legal

# ---------------------------------------------------
# DATABASE CHECK
# ---------------------------------------------------

contracts = {
    "employment_contract": "data/employment_contract.txt",
    "rental_contract": "data/rental_contract.txt",
    "nda_contract": "data/nda_contract.txt",
    "service_contract": "data/service_contract.txt"
}

for collection_name, contract_path in contracts.items():

    if not collection_has_data(collection_name):

        print(f"{collection_name} missing. Running ingestion...")

        ingest_contracts({
            collection_name: contract_path
        })

if not collection_has_data("legal_knowledge"):

    print("legal_knowledge missing. Running legal ingestion...")

    ingest_legal()

from utils.prompt_builder import build_prompt

from utils.llm import generate_answer

from utils.source_formatter import (
    extract_clause_titles,
    extract_legal_titles
)
# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="LexClause",
    page_icon="⚖️",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------

st.markdown("""
<style>

/* ---------------------------------------------------
MAIN BACKGROUND
--------------------------------------------------- */

.main {
    background-color: #0b1120;
}

/* ---------------------------------------------------
GLOBAL SPACING
--------------------------------------------------- */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* ---------------------------------------------------
TYPOGRAPHY
--------------------------------------------------- */

h1 {
    color: #f8fafc;
    font-size: 3rem !important;
    font-weight: 700 !important;
}

h2, h3 {
    color: #f8fafc;
}

.small-muted {
    color: #94a3b8;
    font-size: 1rem;
    line-height: 1.6;
}

/* ---------------------------------------------------
MODE BADGE
--------------------------------------------------- */

.mode-badge {
    display: inline-block;
    padding: 0.4rem 0.9rem;
    border-radius: 999px;
    background-color: #1e3a8a;
    color: white;
    font-size: 0.85rem;
    font-weight: 600;
    margin-top: 0.5rem;
    margin-bottom: 1.2rem;
}

/* ---------------------------------------------------
TEXT INPUT
--------------------------------------------------- */

.stTextInput > div > div > input {
    background-color: #111827;
    color: white;
    border-radius: 12px;
    border: 1px solid #334155;
    padding: 14px;
    font-size: 1rem;
}

/* ---------------------------------------------------
SELECT BOX
--------------------------------------------------- */

.stSelectbox div[data-baseweb="select"] {
    background-color: #111827;
    border-radius: 12px;
    border: 1px solid #334155;
    cursor: pointer !important;
}

.stSelectbox div[data-baseweb="select"] * {
    cursor: pointer !important;
}

/* ---------------------------------------------------
BUTTON
--------------------------------------------------- */

.stButton > button {
    background-color: #1d4ed8;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #2563eb;
    transform: translateY(-1px);
}

/* ---------------------------------------------------
ANSWER CARD
--------------------------------------------------- */

.answer-box {
    background-color: #111827;
    padding: 1.8rem;
    border-radius: 18px;
    border: 1px solid #334155;
    margin-bottom: 1rem;
    line-height: 1.9;
    font-size: 1.02rem;
    color: #f1f5f9;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.02);
}

/* ---------------------------------------------------
SOURCE CARDS
--------------------------------------------------- */

.source-box {
    background-color: #0f172a;
    padding: 1rem;
    border-radius: 14px;
    border: 1px solid #334155;
    margin-bottom: 1rem;
    color: #e2e8f0;
    line-height: 1.7;
}

/* ---------------------------------------------------
SOURCE HEADER CARD
--------------------------------------------------- */

.source-card {
    background-color: #111827;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
}

.source-title {
    font-size: 1rem;
    font-weight: 600;
    color: #f8fafc;
}

.source-subtitle {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 0.2rem;
}

/* ---------------------------------------------------
SESSION BANNER
--------------------------------------------------- */

.session-banner {

    display: flex;
    align-items: center;
    gap: 16px;

    background: #111827;

    border: 1px solid #334155;

    border-radius: 12px;

    padding: 10px 16px;

    margin-top: 8px;
    margin-bottom: 18px;

    font-size: 0.95rem;
}

.status-ready {

    color: #4ade80;
    font-weight: 600;

}

/* ---------------------------------------------------
CLAUSE PANEL
--------------------------------------------------- */

.clause-panel {
    border-left: 4px solid #2563eb;
}

/* ---------------------------------------------------
LEGAL PANEL
--------------------------------------------------- */

.legal-panel {
    border-left: 4px solid #d4a017;
}

/* ---------------------------------------------------
HISTORY
--------------------------------------------------- */

.history-box {
    background-color: #0f172a;
    padding: 1rem;
    border-radius: 14px;
    border: 1px solid #1e293b;
    margin-bottom: 1rem;
    line-height: 1.7;
    color: #e2e8f0;
}

/* ---------------------------------------------------
EMPTY STATE
--------------------------------------------------- */

.empty-state {
    background-color: #111827;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 2rem;
    margin-top: 2rem;
    color: #cbd5e1;
    line-height: 1.8;
}

/* ---------------------------------------------------
EXPANDERS
--------------------------------------------------- */

.streamlit-expanderHeader {
    font-weight: 600;
    color: #f8fafc !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.header("⚙️ Session Settings")

    mode = st.selectbox(
        "Assistant Mode",
        [
            "General User",
            "Professional"
        ]
    )

    contract_type = st.selectbox(
        "Contract Type",
        [
            "Employment Agreement",
            "Residential Rental Agreement",
            "Mutual Non-Disclosure Agreement (NDA)",
            "Service Agreement"
        ]
    )

    collection_map = {
        "Employment Agreement": "employment_contract",
        "Residential Rental Agreement": "rental_contract",
        "Mutual Non-Disclosure Agreement (NDA)": "nda_contract",
        "Service Agreement": "service_contract"
    }

    selected_collection = collection_map[contract_type]

    st.markdown("---")

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("⚖️ LexClause")

st.markdown(
    """
    <div class="small-muted">
    AI-powered legal assistant for analyzing employment, residential rental,
    non-disclosure, and service agreements using semantic retrieval and
    relevant provisions of the Indian Contract Act, 1872.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.markdown(
    f"""
<div class="session-banner">
    <span>📄 <b>{contract_type}</b></span>
    <span>•</span>
    <span>⚖️ <b>{mode}</b></span>
    <span>•</span>
    <span class="status-ready">🟢 Knowledge Base Ready</span>
</div>
""".strip(),
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)




# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "latest_answer" not in st.session_state:
    st.session_state.latest_answer = ""

if "latest_clause_titles" not in st.session_state:
    st.session_state.latest_clause_titles = []

if "latest_clauses" not in st.session_state:
    st.session_state.latest_clauses = []

if "latest_legal_titles" not in st.session_state:
    st.session_state.latest_legal_titles = []

if "latest_legal_sections" not in st.session_state:
    st.session_state.latest_legal_sections = []

# ---------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------

question = st.chat_input(
    "Ask a question about the selected contract..."
)

submitted = question is not None

# ---------------------------------------------------
# GENERATION PIPELINE
# ---------------------------------------------------

if submitted and question:

    with st.spinner(
        "Analyzing contract and legal provisions..."
    ):

        # Embedding
        query_embedding = generate_query_embedding(
            question
        )

        # Clause retrieval
        clause_results = search_clauses(
            query_embedding,
            selected_collection
        )

        retrieved_clauses = clause_results["documents"][0]
        retrieved_clauses = rerank_results(
            question,
            retrieved_clauses,
            top_k=3
        )

        # Legal retrieval
        legal_results = search_legal_sections(
            query_embedding
        )

        retrieved_legal_sections = legal_results["documents"][0]
        retrieved_legal_sections = rerank_results(
            question,
            retrieved_legal_sections,
            top_k=2
   )

        # Prompt
        prompt = build_prompt(
            question,
            retrieved_clauses,
            retrieved_legal_sections,
            st.session_state.conversation_history[-3:],
            mode
        )

        # LLM Answer
        answer = generate_answer(prompt)

        # Conversation memory
        st.session_state.conversation_history.append(
            {
                "user": question,
                "assistant": answer
            }
        )

        # Source titles
        clause_titles = extract_clause_titles(
            retrieved_clauses
        )
    
        legal_titles = extract_legal_titles(
            retrieved_legal_sections
        )

        # Persist UI state
        st.session_state.latest_answer = answer

        st.session_state.latest_clause_titles = (
            clause_titles
        )

        st.session_state.latest_clauses = (
            retrieved_clauses
        )
        
        st.session_state.latest_legal_titles = (
            legal_titles
        )

        st.session_state.latest_legal_sections = (
            retrieved_legal_sections
        )

# ---------------------------------------------------
# EMPTY STATE
# ---------------------------------------------------

if not st.session_state.latest_answer:

    st.markdown(
        """
        <div class="empty-state">

        <h3>Welcome to LexClause</h3>

        Ask questions about:
        <ul>
        <li>Employment agreements</li>
        <li>Residential rental agreements</li>
        <li>Non-disclosure agreements (NDAs)</li>
        <li>Service agreements</li>
        <li>Contract obligations, payments, confidentiality, termination, and dispute resolution</li>
        </ul>

        The assistant retrieves:
        <ul>
        <li>Relevant contract clauses</li>
        <li>Applicable provisions of the Indian Contract Act, 1872</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )
# ---------------------------------------------------
# RENDER CONVERSATION
# ---------------------------------------------------

if st.session_state.conversation_history:

    for chat in st.session_state.conversation_history:

        # ---------------------------------------------------
        # USER MESSAGE
        # ---------------------------------------------------

        st.markdown(
            f"""
            <div class="history-box">
                <b>👤 You</b><br><br>
                {chat['user']}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------------------------------------------------
        # ASSISTANT MESSAGE
        # ---------------------------------------------------

        st.markdown(
            f"""
            <div class="answer-box">
                <b>⚖️ LexClause</b><br><br>
                {chat['assistant']}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------------------------------------------------
        # CONTRACT SOURCES
        # ---------------------------------------------------

        if chat.get("clauses"):

            st.markdown(
                "### 📄 Contract Clauses"
            )

            for title, clause in zip(
                chat.get("clause_titles", []),
                chat.get("clauses", [])
            ):

                st.markdown(
                    f"""
                    <div class="source-card">
                        <div class="source-title">
                            {title}
                        </div>
                        <div class="source-subtitle">
                            Contract clause supporting this answer.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                with st.expander("View Clause"):

                    st.markdown(
                        f"""
                        <div class="source-box clause-panel">
                            {clause}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # ---------------------------------------------------
        # LEGAL SOURCES
        # ---------------------------------------------------

        if chat.get("legal_sections"):

            st.markdown(
                "### ⚖️ Legal Provisions"
            )

            for title, section in zip(
                chat.get("legal_titles", []),
                chat.get("legal_sections", [])
            ):

                st.markdown(
                    f"""
                    <div class="source-card">
                        <div class="source-title">
                            {title}
                        </div>
                        <div class="source-subtitle">
                            Legal provision supporting this answer.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                with st.expander("View Provision"):

                    st.markdown(
                        f"""
                        <div class="source-box legal-panel">
                            {section}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        st.markdown("---")
   