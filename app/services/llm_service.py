import os
import requests
import google.generativeai as genai
from .prompts import RAG_PROMPT_TEMPLATE

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def call_ollama(prompt: str):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.HTTPError as e:
        error_msg = e.response.text if e.response else str(e)
        print(f"Ollama HTTP error: {error_msg}")
        return "Sorry, unable to generate answer. Both Gemini and Ollama are unavailable."
    except Exception as e:
        print(f"Ollama fallback failed: {e}")
        return "Sorry, unable to generate answer. Both Gemini and Ollama are unavailable."


def generate_answer(query: str, chunks: list[dict]):

    context_parts = []
    for i, chunk in enumerate(chunks[:3]):
        url = chunk.get("url", chunk.get("doc_path", "Unknown Source"))
        text = chunk["chunk_text"]
        context_parts.append(f"Source [{i+1}] (URL: {url}):\n{text}")
        
    context = "\n\n".join(context_parts)

    prompt = RAG_PROMPT_TEMPLATE.format(query=query, context=context)
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key.strip() == "":
            print("Google API Key not found or empty, falling back to Ollama")
            return call_ollama(prompt)
            
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini generation failed: {e}. Falling back to Ollama.")
        return call_ollama(prompt)