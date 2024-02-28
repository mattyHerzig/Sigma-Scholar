from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.core.extractors import (
    QuestionsAnsweredExtractor,
    TitleExtractor,
    KeywordExtractor,
)
from llama_index.extractors.entity import EntityExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from llama_index.program.openai import OpenAIPydanticProgram
from llama_index.core.extractors import PydanticProgramExtractor
from typing import List
from pydantic import BaseModel, Field, validator
from llama_index.readers.web import SimpleWebPageReader
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
import nest_asyncio

import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
load_dotenv()  # take environment variables from .env.

llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
db1 = chromadb.PersistentClient(path="./chroma_db")
collection = db1.get_or_create_collection("scholarship_nodes")
vector_store = ChromaVectorStore(chroma_collection=collection)

def get_web(url):
    webpage = SimpleWebPageReader(html_to_text=True).load_data(
        [url]
    )
    print(webpage[0].text)
    return webpage


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
    entities:         str = Field(..., description="Unique entities in this text chunk.")
    keywords:         str = Field(..., description="Summative keywords in this text chunk.")
    categories:       str = Field(..., description="categories in this text chunk")
    
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
    """Object representing a list of multiple Scholarships."""

    scholarships: List[Scholarship] = Field(..., description="List of scholarships.")



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



parser = SentenceSplitter(
    chunk_size=1024,
    chunk_overlap=20,
)

openai_program = OpenAIPydanticProgram.from_defaults(
    output_cls=Scholarship,
    prompt_template_str="{input}",
    # extract_template_str=EXTRACT_TEMPLATE_STR
)

program_extractor = PydanticProgramExtractor(
    program=openai_program, input_key="input", show_progress=True
)

nest_asyncio.apply()

def pipeline_mod(nodes):
    new_nodes = program_extractor.process_nodes(nodes)
    embed_model=OpenAIEmbedding()
    for node in new_nodes:
        node_embedding = embed_model.get_text_embedding(
            node.get_content(metadata_mode="all")
        )
        node.embedding = node_embedding
        print(node.metadata)
    vector_store.add(new_nodes)

def pipeline_single(node):
    new_node = program_extractor.extract(node)
    embed_model=OpenAIEmbedding()
    for node in new_node:
        node_embedding = embed_model.get_text_embedding(
            node.get_content(metadata_mode="all")
        )
        node.embedding = node_embedding
        print(node.metadata)
    vector_store.add(new_node)

def read_and_chunk(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    chunks = [content.strip()]
    # Remove empty strings from the list of chunks
    return chunks

# file_path = "single.txt"  # Replace with your file path
# result_chunks = read_and_chunk(file_path)
result_chunks =["""Scholarship: Greater St. Louis Art Association Scholarship
categories: [act score, act scores from 16 to 20]
 website url:https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/act-score/act-scores-from-16-to-20/greater-st-louis-art-association-scholarship
 Extracted from website:
page-name: Greater St. Louis Art Association Scholarship
description: The Greater St. Louis Art Association is offering scholarships to college students in the St. Louis area who are majoring in Art. Scholarships are one-time awards up to $2500 per student. Eligible applicants must be a full or half-time college student (minimum of 6 credit hours) majoring in an art discipline, and applicants must must submit a fully completed application with six images of their recent artwork in a PowerPoint file (see website for more details). Winners are notified by March 20.""",
"""Scholarship: Alfred State All-American Scholarship
categories: [act score, act scores from 21 to 25]
 website url:https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/act-score/act-scores-from-21-to-25/alfred-state-all-american-scholarship
 Extracted from website:
page-name: Alfred State All-American Scholarship
description: The Alfred State All-American Scholarship is offered to incoming freshmen who possess an ACT of 24 or an SAT of 1220, as well as a 3.3 GPA. Students are required to earn a cumulative 3.0 GPA each semester to maintain this scholarship. Students must live on campus and be legal US residents."""]
documents = [Document(text=t) for t in result_chunks]
nodes = parser.get_nodes_from_documents(documents, show_progress=True)
pipeline_single(nodes)

index = VectorStoreIndex.from_vector_store(vector_store)


query_engine = index.as_query_engine(
    output_cls=Scholarships, response_mode="compact", llm=llm
)
scholarship="Fukunaga Scholarship Foundation"
prompt = f"give me scholarships"
response = query_engine.query(prompt)
print(response)



    
