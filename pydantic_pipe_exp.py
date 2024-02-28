from typing import List

from pydantic import BaseModel, Field

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

documents=get_web("https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/employer/california-grape-grower/cwggf-scholarship")
index = VectorStoreIndex.from_documents(
    documents,
)

## set the structured output class
class Scholarship(BaseModel):
    """Object representing a single scholarship."""

    name: str = Field(..., description="Name of the scholarship.")
    amount: str = Field(..., description="Funding of the scholarship.")
    deadline: str = Field(..., description="deadline of the scholarship")
    description: str = Field(..., description="description of the scholarship or None")
    link: str = Field(..., description="link of the scholarship or None")
    


class Scholarships(BaseModel):
    """Object representing a list of Scholarships."""

    scholarships: List[Scholarship] = Field(..., description="List of scholarships.")



query_engine = index.as_query_engine(
    output_cls=Scholarships, response_mode="compact", llm=llm
)
scholarship="CWGGF Scholarship"
prompt = f"What are the main details about the {scholarship} scholarship"
response = query_engine.query(prompt)

print(response)
# > 'Paul Graham'
# print(response.best_known_for)
# # > ['working on Bel', 'co-founding Viaweb', 'creating the programming language Arc']
# print(response.extra_info)
# # > "Paul Graham is a computer scientist, entrepreneur, and writer. He is best known      for ..."