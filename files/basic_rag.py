from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.core.extractors import (
    QuestionsAnsweredExtractor,
    TitleExtractor,
)
from llama_index.core.ingestion import IngestionPipeline
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from llama_index.core.tools import QueryEngineTool

from typing import List

from pydantic import BaseModel, Field, validator

# from llama_index.readers.web import SimpleWebPageReader
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.response.pprint_utils import pprint_response
from llama_index.llms.openai import OpenAI

import nest_asyncio
nest_asyncio.apply()


load_dotenv()  # take environment variables from .env.

llm = OpenAI(temperature=0, model="gpt-4")
db1 = chromadb.PersistentClient(path="./chroma_db")
collection = db1.get_or_create_collection("scholarship_nodes")
vector_store = ChromaVectorStore(chroma_collection=collection)



# documents=get_web("https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/employer/california-grape-grower/cwggf-scholarship")

## set the structured output class
class Scholarship(BaseModel):
    """Object representing a single scholarship."""    
    name:             str = Field(..., description="name of the scholarship.")
    amount:           str = Field(..., description="amount of money offered by the scholarship.")
    deadline:         str = Field(..., description="deadline of the scholarship")
    awards_available: str = Field(..., description="number of awards available (or \"Varies\")")
    backlink:         str = Field(..., description="backlink to the scholarship")
    description:      str = Field(..., description="concise summary of scholarship qualifications")
    gender:           str = Field(..., description="scholarship gender qualification")
    GPA:              str = Field(..., description="scholarship minimum (initial, not renewable) GPA qualification")
    SAT:              str = Field(..., description="scholarship minimum SAT qualification")
    ACT:              str = Field(..., description="scholarship minimum ACT qualification")
    age:              str = Field(..., description="scholarship age qualification")
    citizenship:      str = Field(..., description="scholarship citizenship qualification")
    race:             str = Field(..., description="scholarship race/ethnicity qualification")
    disability:       str = Field(..., description="scholarship disability qualification")
    character_trait:  str = Field(..., description="scholarship character trait qualification")
    financial_status:  str = Field(..., description="scholarship financial status qualification")
    residence:        str = Field(..., description="scholarship location of residence qualification in US format e.g. City, State")
    school_k12:       str = Field(..., description="scholarship school K–12 related qualification")
    school_college:   str = Field(..., description="scholarship school college related qualification")
    extracurriculars: str = Field(..., description="scholarship extracurriculars qualification")
    organization:     str = Field(..., description="scholarship organization qualification")
    work_experience:  str = Field(..., description="scholarship work experience qualification")
    career:           str = Field(..., description="scholarship career/employer qualification")
    
    @validator("amount", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("deadline", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("backlink", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("description", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("GPA", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("gender", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("age", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("citizenship", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("race", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("disability", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("character_trait", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("financial_status", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("residence", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("SAT", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("ACT", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("school_k12", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("school_college", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("extracurriculars", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("organization", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("work_experience", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    @validator("career", pre=True)
    def none_to_empty(cls, v: object) -> object:
        return "" if v is None else v
    



class Scholarships(BaseModel):
    """Object representing a list of Scholarships."""

    scholarships: List[Scholarship] = Field(..., description="List of scholarships.")


# index = VectorStoreIndex.from_documents(
#     documents,
# )







def get_text_from_elements(url, element_ids):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get text from elements with specified IDs
        element_texts = {}
        for element_id in element_ids:
            element = soup.find(id=element_id)
            if element:
                element_texts[element_id] = element.get_text().strip()
        
        return element_texts
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return {}
    
def replace_hyphens_with_space(input_string):
    parts = input_string.split('-')
    modified_parts = [part.replace('-', ' ') for part in parts]
    result = ' '.join(modified_parts)
    return result

def get_subdirectories(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Get the path components
    path_components = parsed_url.path.split('/')
    
    # Filter out empty path components
    subdirectories = [replace_hyphens_with_space(component) for component in path_components if component]
    
    return subdirectories

def extract_page(link):
    extract_dict = ["page-name", "header-items-award-detail-inner-wrapper", "description"]
    
    element_texts = get_text_from_elements(link, extract_dict)
    first_key = next(iter(element_texts))
    first_value = element_texts [first_key]
    subs=get_subdirectories(link)
    # Display the extracted text
    output=f"""Scholarship: {first_value}\ncategories: [{subs[-3]}, {subs[-2]}]\n backlink url:{link}\n Extracted from website:\n"""
    
    for element_id, text in element_texts.items():
        output+=f"{element_id}: {text.strip()}\n"
        
    return output


# build index
# index = VectorStoreIndex.from_documents(documents)


# load documents
# ...

# parse nodes
parser = SentenceSplitter(
    chunk_size=1024,
    chunk_overlap=20,
)

def pipeline(nodes):
    extractors = [
    TitleExtractor(nodes=5, llm=llm),
    QuestionsAnsweredExtractor(questions=3, llm=llm),]
    pipe = IngestionPipeline(
        transformations=extractors,
    )
    newnodes = pipe.run(nodes=nodes, in_place=False)
    embed_model=OpenAIEmbedding()
    for node in newnodes:
        node_embedding = embed_model.get_text_embedding(
            node.get_content(metadata_mode="all")
        )
        node.embedding = node_embedding
    vector_store.add(newnodes)


index = VectorStoreIndex.from_vector_store(vector_store)


query_engine = index.as_query_engine(
    output_cls=Scholarships, response_mode="compact", llm=llm
)

query_tool_scholarship = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="scholarships",
    description=(
        f"Provides information about scholarships and attributes"
        f" such as name, amount, deadline, awards available, backlink"
    ),
)
# define query plan tool
from llama_index.core.tools import QueryPlanTool
from llama_index.core import get_response_synthesizer

response_synthesizer = get_response_synthesizer()
query_plan_tool = QueryPlanTool.from_defaults(
    query_engine_tools=[query_tool_scholarship],
    response_synthesizer=response_synthesizer,
)
query_plan_tool.metadata.to_openai_tool()

from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI

agent = OpenAIAgent.from_tools(
    [query_plan_tool],
    max_function_calls=10,
    llm=OpenAI(temperature=0, model="gpt-4-0613"),
    verbose=True,
)

response = agent.query("What scholarships are available?")

# scholarship=""
# prompt = f"What are the main details for each of the {scholarship}scholarships"
# response = query_engine.query(prompt)
print(response)

