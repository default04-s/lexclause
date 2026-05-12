def build_prompt(
    query,
    retrieved_clauses,
    retrieved_legal_sections,
    conversation_history,
    mode
):

    clause_context = "\n\n".join(retrieved_clauses)

    legal_context = "\n\n".join(retrieved_legal_sections)

    history_text = ""

    for item in conversation_history:

        history_text += f"""
User: {item['user']}
Assistant: {item['assistant']}
"""

    # ---------------------------------------------------
    # MODE INSTRUCTIONS
    # ---------------------------------------------------

    if mode == "General User":

        mode_instruction = """
Explain answers in simple and practical language.

Avoid heavy legal jargon unless necessary.

Focus on:
- what the clause means
- practical consequences
- what the user should understand

Keep explanations concise and easy to understand.
"""

    else:

        mode_instruction = """
Provide legally detailed explanations.

Use legal terminology where appropriate.

Clearly reference:
- agreement clauses
- legal provisions
- legal reasoning

Maintain professional legal tone.
"""

    # ---------------------------------------------------
    # FINAL PROMPT
    # ---------------------------------------------------

    prompt = f"""
You are a legal assistant specialized in rental agreements and Indian contract law.

IMPORTANT RULES:
{mode_instruction}

Always:
- answer using retrieved context only
- avoid unsupported claims
- answer cautiously if information is incomplete
- clearly mention legal references when applicable

CONVERSATION HISTORY:
{history_text}

CURRENT USER QUESTION:
{query}

RETRIEVED RENTAL AGREEMENT CLAUSES:
{clause_context}

RETRIEVED LEGAL PROVISIONS:
{legal_context}

ANSWER:
"""

    return prompt