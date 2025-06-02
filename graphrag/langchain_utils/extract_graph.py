from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))

EXTRACTION_PROMPT = """
Extract (subject, relation, object) triples from the following text.

Text:
{text}

Return the results as a list of triples like:
(subject1, relation1, object1)
(subject2, relation2, object2)
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
