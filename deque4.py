import concurrent.futures

import collections
from collections import deque

import multiprocessing
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
parser = SentenceSplitter(
    chunk_size=1024,
    chunk_overlap=20,
)
nest_asyncio.apply()

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



openai_program = OpenAIPydanticProgram.from_defaults(
    output_cls=Scholarship,
    prompt_template_str="{input}",
)
program_extractor = PydanticProgramExtractor(
    program=openai_program, input_key="input", show_progress=True
)

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
# Define your Document, parser, and pipeline_mod functions here


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures
from tqdm import tqdm

def get_links_from_webpage(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get all the links in the main body of the webpage
        dir_list_div = soup.find('div', {'id': 'dir-list'})
        
        # Get all the links within the "dir-list" div
        links = []
        if dir_list_div:
            for anchor_tag in dir_list_div.find_all('a'):
                href = anchor_tag.get('href')
                if href:
                    full_url = urljoin(url, href)
                    links.append(full_url)
        
            return links
        else:
            print("No div with id 'dir-list' found on the webpage.")
            return []
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return []



def get_links_with_blacklink_class(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get all the links within <a> elements with a class containing "blacklink"
        blacklink_links = []
        for anchor_tag in soup.find_all('a', class_=lambda x: x and 'blacklink' in x):
            href = anchor_tag.get('href')
            if href:
                full_url = urljoin(url, href)
                blacklink_links.append(full_url)
        
        return blacklink_links
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return []

def get_links_from_table(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get all the links within the <table>
        table_links = []
        for table_row in soup.find_all('tbody'):
            for anchor_tag in table_row.find_all('a'):
                href = anchor_tag.get('href')
                if href:
                    full_url = urljoin(url, href)
                    table_links.append(full_url)
        
        return table_links
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return []






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
    output=f"""Scholarship: {first_value}\ncategories: [{subs[-3]}, {subs[-2]}]\n website url:{link}\n Extracted from website:\n"""
    
    for element_id, text in element_texts.items():
        output+=f"{element_id}: {text.strip()}\n"
        
    return output

# define others

def process_batch(batch):
    documents = [Document(text=t) for t in batch]
    nodes = parser.get_nodes_from_documents(documents)
    pipeline_mod(nodes)

def process_link(link, shared_deque, batch_size):
    top = get_subdirectories(link)[-1]
    blacklink_links = get_links_with_blacklink_class(link)

    for blacklink in blacklink_links:
        if not "military" in blacklink:
            mid = get_subdirectories(blacklink)[-1]
            table_links = get_links_from_table(blacklink)
            for tablelink in table_links:
                low = get_subdirectories(tablelink)[-1]
                print(f"{top} : {mid} : {low}")
                shared_deque.append(extract_page(tablelink))

                if len(shared_deque) >= batch_size:
                    # Process the batch using multiprocessing
                    batch = list(shared_deque)
                    shared_deque.clear()

                    with multiprocessing.Pool() as pool:
                        pool.map(process_batch, [batch])
        else:
            mid = get_subdirectories(blacklink)[-1]
            table_links = get_links_from_table(blacklink)
            for tablelink in table_links:
                low = get_subdirectories(tablelink)[-1]
                print(f"{top} : {mid} : {low}")
                shared_deque.append(extract_page(tablelink))

                if len(shared_deque) >= batch_size:
                    # Process the batch using multiprocessing
                    batch = list(shared_deque)
                    shared_deque[:] = []

                    with multiprocessing.Pool() as pool:
                        pool.map(process_batch, [batch])


def send_pages_to_deque(origin_link, shared_deque, batch_size):
    links = get_links_from_webpage(origin_link)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Process each link concurrently
        futures = [executor.submit(process_link, link, shared_deque, batch_size) for link in links]

        # Wait for all threads to complete
        concurrent.futures.wait(futures)

    # Process any remaining items in the deque
    if len(shared_deque) > 0:
        batch = list(shared_deque)
        shared_deque[:] = []  # Clear the deque

        with multiprocessing.Pool() as pool:
            pool.map(process_batch, [batch])

    print("Progress: All links processed and added to the deque.")

def main():
    origin_link = 'https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory'  # Replace with your actual URL
    batch_size = 20
    shared_deque = deque()

    links = get_links_from_webpage(origin_link)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Process each link concurrently
        futures = [executor.submit(process_link, link, shared_deque, batch_size) for link in links]

        # Add tqdm to visualize the progress of processing links
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing Links"):
            future.result()

    # Process any remaining items in the deque
    if shared_deque:
        batch = list(shared_deque)
        shared_deque[:] = []

        with multiprocessing.Pool() as pool:
            pool.map(process_batch, [batch])

    print("Progress: All links processed and added to the deque.")

if __name__ == "__main__":
    main()