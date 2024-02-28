from flask import Flask, request, jsonify
from flask_cors import CORS

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
import asyncio

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

index = VectorStoreIndex.from_vector_store(vector_store)


query_engine = index.as_query_engine(
    output_cls=Scholarships, response_mode="compact", llm=llm
)

query_tool_scholarship = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="scholarships",
    description=(
        f"Provides a list of scholarships and their qualification attributes"
        f" such as deadline, funding amount, links, gender, ethnicity, state"
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
    llm=OpenAI(temperature=0, model="gpt-3.5-turbo"),
    verbose=True,
)


app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

@app.route('/rag-query', methods=['GET'])
async def get_message():
    # Retrieve query parameters
    query = request.args.get('query','help')
    # scholarshipAmount = request.args.get('scholarshipAmount','Varies')
    # gpa = request.args.get('gpa','0')
    # satScore = request.args.get('satScore','0')
    # actScore = request.args.get('actScore','0')
    # stateOrCountry = request.args.get('stateOrCountry','0')
    # citizenship = request.args.get('citizenship','0')
    # educationLevel = request.args.get('educationLevel','0')
    # gender = request.args.get('gender','0')
    # age = request.args.get('age','0')
    # familyIncome = request.args.get('familyIncome','0')
    # financialAidEligibility = request.args.get('financialAidEligibility','0')
    # militaryAffiliation = request.args.get('militaryAffiliation','0')
    # raceEthnicity = request.args.get('raceEthnicity','0')
    
    ragquery = f" Using the scholarship database, answer the user's question as a guidance counselor: {query}"
    # Return a message incorporating the query parameters
    response = agent.query(ragquery)
    print(response)
    return jsonify({"message": f"{response}"})

@app.route('/post-data', methods=['POST'])
async def post_data():
    data = request.json  # Get JSON data sent with POST request
    print(data)
    message = data.get('message','help')
    # Retrieve query parameters
    # scholarshipAmount = data.get('scholarshipAmount','Varies')
    # gpa = data.get('gpa','0')
    # satScore = data.get('satScore','0')
    # actScore = data.get('actScore','0')
    # stateOrCountry = data.get('stateOrCountry','0')
    # citizenship = data.get('citizenship','0')
    # educationLevel = data.get('educationLevel','0')
    # gender = data.get('gender','0')
    # age = data.get('age','0')
    # familyIncome = data.get('familyIncome','0')
    # financialAidEligibility = data.get('financialAidEligibility','0')
    # militaryAffiliation = data.get('militaryAffiliation','0')
    # raceEthnicity = data.get('raceEthnicity','0')
    
    # ragquery = f"gpa of {gpa}, sat score of {satScore}, act score of {actScore}, and im looking for scholarship amount around {scholarshipAmount}, I am from state or country {stateOrCountry}, my citizenship is {citizenship}, my education level is {educationLevel}"
    # Return a message incorporating the query parameters
    # Print the received data on the Flask server console
    response = agent.query(message)
    print(response)
    return jsonify({"message": f"Hello, {response}"})

if __name__ == '__main__':
    app.run(debug=True)
