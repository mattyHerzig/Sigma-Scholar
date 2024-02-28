from dotenv import load_dotenv
from llama_index.core import (
    PromptTemplate,  
    VectorStoreIndex,
    SimpleDirectoryReader,
    SummaryIndex,
    Settings,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.extractors import (
    KeywordExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
)
from llama_index.core.indices.service_context import ServiceContext
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.node_parser import SemanticSplitterNodeParser, SentenceSplitter, TokenTextSplitter
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.vector_stores.chroma import ChromaVectorStore
from pydantic import BaseModel, Field
from typing import List
import llama_index
import pydantic

import chromadb
import nest_asyncio
nest_asyncio.apply()

# take environment variables from .env.
load_dotenv()  

# set the model
llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo", max_tokens=512)

# set our index / storage for the nodes
db1 = chromadb.PersistentClient(path="./chroma_db")
collection = db1.get_or_create_collection("scholarship_nodes")
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
embed_model=OpenAIEmbedding()
index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=embed_model,
)

# set the index/engine
query_engine = index.as_query_engine(verbose=True)

#rag mode (ignore for now)
# semantic_query_engine = index.as_chat_engine(
#     service_context=service_context, chat_mode="react", verbose=True)

# set embeddings

# get the documents
def get_web(url):
    # loader = SimpleWebPageReader()
    # documents = loader.load_data(urls=['https://google.com'])
    webpage = SimpleWebPageReader(html_to_text=True).load_data(
        [url]
    )
    print(webpage[0].text)
    return webpage

# Optional: beautiful soup get hardcode option

#Ingestion pipeline section
def semanticPipe(in_doc):
    ## choose splitters
    # splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)


    # splitter = SemanticSplitterNodeParser(
    #     buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
    # )
    ## choose extractors
    # extractors = [
    #     TitleExtractor(nodes=5, llm=llm),
    #     QuestionsAnsweredExtractor(questions=3, llm=llm),
    #     KeywordExtractor(keywords=10, llm=llm),
    #     EntityExtractor(
    #     prediction_threshold=0.5,
    #     label_entities=False,  # include the entity label in the metadata
    # )]
    
    #init pipe (extracts and they go into db)
    # pipeline = IngestionPipeline(transformations=[splitter]+extractors,
    # vector_store=vector_store)
    pipeline = IngestionPipeline(transformations=[TokenTextSplitter()])
    #run pipe
    nodes = pipeline.run(documents=in_doc)
    for node in nodes:
        print(f"Node: {node.text, node.metadata}\n\n")
        print(node.metadata, '\n\n\n\n')
        print(node.metadata.get('entities'), '\n\n\n\n')
    return nodes

#End Ingestion pipeline section



## set the structured output class
class Scholarship(BaseModel):
    """Object representing a single movie."""

    name: str = Field(..., description="Name of the Scholarship.")
    year: int = Field(..., description="Year of the Scholarship.")


class Scholarships(BaseModel):
    """Object representing a list of Scholarships."""

    scholarships: List[Scholarship] = Field(..., description="List of scholarships.")



testvars=['name','year']

#Query pipeline section
def queryPipe(website_name,vars):

    output_parser = PydanticOutputParser(Scholarships)
    json_prompt_str = """\
    Please get the following variables about the {website_name} scholarship:
    {get_vars}
    Output with the following JSON format: 
    """
    json_prompt_str = output_parser.format(json_prompt_str)

    json_prompt_tmpl = PromptTemplate(json_prompt_str)

    p = QueryPipeline(chain=[json_prompt_tmpl, llm, output_parser], verbose=True)

    ## this is where you put the variables in for the template
    output = p.run(scholarship_name=website_name, get_vars=vars)
    print(output)
    #write json to file 

#End Query pipeline section



#fill db
nodes = semanticPipe(get_web("http://paulgraham.com/worked.html"))
index = VectorStoreIndex(nodes, storage_context=storage_context)
response = query_engine.query("what is the author's name?")
#testing for later: https://www.careeronestop.org/Toolkit/Training/find-scholarships-detail.aspx?lang=en&scholarshipId=2015400
print(response)
