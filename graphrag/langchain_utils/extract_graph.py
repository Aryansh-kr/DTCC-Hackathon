from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))

EXTRACTION_PROMPT = """
You are an expert information extraction agent.

Your task is to extract knowledge triplets from the following text in the format:
(Subject, Predicate, Object)

Each triplet should represent a factual and unambiguous relationship.

Rules:
1. Use concise noun phrases for subjects and objects.
2. Use active voice and verb phrases for predicates (e.g., "works at", "located in", "authored").
3. Normalize entities where possible (e.g., "Google Inc." → "Google").
4. Exclude subjective or uncertain statements (e.g., opinions).
5. Ensure each triplet is standalone and informative.



Output Format (as JSON):
[
  {"subject": "...", "predicate": "...", "object": "..."},
  ...
]
"""

prompt = PromptTemplate(
    input_variables=["text"],
    template=EXTRACTION_PROMPT
)

def extract_triples(text):
    formatted_prompt = prompt.format(text=text)
    response = llm.predict(formatted_prompt)
    
    # crude parsing — in practice use a parser or JSON output format
    triples = []
    for line in response.strip().split("\n"):
        if line.startswith("(") and line.endswith(")"):
            parts = line.strip("()").split(",")
            if len(parts) == 3:
                triples.append(tuple(part.strip().strip('"') for part in parts))
    return triples
