from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse



from typing import List

from pydantic import BaseModel, Field

from llama_index.readers.web import SimpleWebPageReader
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

# documents=get_web("https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/employer/california-grape-grower/cwggf-scholarship")

## set the structured output class
class Scholarship(BaseModel):
    """Object representing a single scholarship."""

    name: str = Field(..., description="Name of the scholarship.")
    amount: str = Field(..., description="Funding Amount of the scholarship.")
    deadline: str = Field(..., description="deadline of the scholarship")
    backlink: str = Field(..., description="link to the scholarship")


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
    output=f"""Scholarship: {first_value}\ncategories: [{subs[-3]}, {subs[-2]}]\n website url:{link}\n Extracted from website:\n"""
    
    for element_id, text in element_texts.items():
        output+=f"{element_id}: {text.strip()}\n"
        
    return output

testlist=['https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/artistic-ability/art-drawing/vpc-community-involvement-and-kathleen-eovino-memorial-scholarship','https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/academic-major/accounting/fukunaga-scholarship-foundation']

outputs=[]
for src in testlist:
    outputs.append(extract_page('https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/artistic-ability/art-drawing/vpc-community-involvement-and-kathleen-eovino-memorial-scholarship'))
print(outputs,'\n\n\n\n')

documents = [Document(text=t) for t in outputs]

# build index
# index = VectorStoreIndex.from_documents(documents)


# load documents
# ...

# parse nodes
parser = SentenceSplitter(
    chunk_size=1024,
    chunk_overlap=20,
)
nodes = parser.get_nodes_from_documents(documents)

# build index
index = VectorStoreIndex(nodes)


query_engine = index.as_query_engine(
    output_cls=Scholarships, response_mode="compact", llm=llm
)
scholarship=""
prompt = f"What are the main details about the {scholarship}scholarships"
response = query_engine.query(prompt)
print(response)

