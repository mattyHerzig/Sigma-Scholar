from typing import List
from pydantic import BaseModel
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)


def get_web(url):
    webpage = SimpleWebPageReader(html_to_text=True).load_data(
        [url]
    )
    print(webpage[0].text)
    return webpage

documents=get_web("http://paulgraham.com/worked.html")
index = VectorStoreIndex.from_documents(
    documents,
)

class Biography(BaseModel):
    """Data model for a biography."""

    name: str
    best_known_for: List[str]
    extra_info: str
    
    
    
query_engine = index.as_query_engine(
    output_cls=Biography, response_mode="compact", llm=llm
)


response = query_engine.query("Who is Paul Graham?")

print(response.name)
# > 'Paul Graham'
print(response.best_known_for)
# > ['working on Bel', 'co-founding Viaweb', 'creating the programming language Arc']
print(response.extra_info)
# > "Paul Graham is a computer scientist, entrepreneur, and writer. He is best known      for ..."