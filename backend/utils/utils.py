import os
from fastapi import HTTPException
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage


def get_llm():
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MAX_TOKENS = os.getenv("MAX_TOKENS")
    if not GOOGLE_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_API_KEY não configurada."
        )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature="0.2",
        # max_output_tokens=MAX_TOKENS,
    )

    return llm