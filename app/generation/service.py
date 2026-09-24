from functools import lru_cache
from groq import Groq

from app.core.config import get_settings


@lru_cache
def get_groq_client() -> Groq:
    return Groq(api_key=get_settings().groq_api_key)


def build_prompt(query: str, retrieved_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(retrieved_chunks)
    return f"""Answer the question using ONLY the context below.
If the context does not contain the answer, say "I don't have enough information to answer that" — do not guess.

Context:
{context}

Question: {query}

Answer:"""


def generate_answer(prompt: str) -> str:
    response = get_groq_client().chat.completions.create(
        model=get_settings().llm_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content or "I don't have enough information to answer that."