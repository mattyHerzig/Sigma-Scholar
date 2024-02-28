# from llama_index import SummaryIndex
# from llama_index.readers import SimpleWebPageReader
# import os
# import openai
# import requests
# from llama_index import SQLDatabase,ServiceContext
# from llama_index.llms import OpenAI
# from llama_index.ingestion import IngestionPipeline
# from llama_index.text_splitter import SentenceSplitter
# from llama_index import Document
# from llama_index.node_parser import SemanticSplitterNodeParser
# from llama_index.embeddings import OpenAIEmbedding
# from llama_index import VectorStoreIndex, StorageContext
# from llama_index.vector_stores import ChromaVectorStore
# from llama_index import SimpleDirectoryReader
# from llama_index.schema import TextNode, NodeRelationship, RelatedNodeInfo
# from llama_index import (
#     ServiceContext,
#     OpenAIEmbedding,
#     PromptHelper,
# )
# from llama_index import (
#     SimpleDirectoryReader,
#     VectorStoreIndex,
#     StorageContext,
#     load_index_from_storage,
# )

# from llama_index.tools import QueryEngineTool, ToolMetadata
# from llama_index.node_parser import HierarchicalNodeParser
# from llama_index.node_parser import get_leaf_nodes, get_root_nodes
# from llama_index.extractors import (
#     SummaryExtractor,
#     QuestionsAnsweredExtractor,
#     TitleExtractor,
#     KeywordExtractor,
#     EntityExtractor,
#     BaseExtractor,
# )
# import nest_asyncio
# nest_asyncio.apply()
# from llama_index.core.query_pipeline import QueryPipeline
# from llama_index.core import PromptTemplate
# from IPython.display import Markdown, display
# from typing import List
# from pydantic import BaseModel, Field
# from llama_index.core.output_parsers import PydanticOutputParser
# from llama_index.llms.openai import OpenAI
# from llama_index.embeddings.openai import OpenAIEmbedding
# from llama_index.core import Settings
# import os
# from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env.


# # set the model
# llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo", max_tokens=512)

# # set our index / storage for the nodes
# db1 = chromadb.PersistentClient(path="./chroma_db")
# semantic_collection = db1.get_or_create_collection("semantic_nodes")
# semantic_vector_store = ChromaVectorStore(chroma_collection=semantic_collection)
# semantic_storage_context = StorageContext.from_defaults(vector_store=semantic_vector_store)
# semantic_service_context = ServiceContext.from_defaults(embed_model=OpenAIEmbedding())
# semantic_index = VectorStoreIndex.from_vector_store(
#     semantic_vector_store,
#     service_context=semantic_service_context,
# )

# # set the index/engine

# semantic_query_engine = semantic_index.as_chat_engine(
#     service_context=semantic_service_context, chat_mode="react", verbose=True)


# # set embeddings
# embed_model = OpenAIEmbedding()

# # get the documents
# def getWeb(url):
    

#     # loader = SimpleWebPageReader()
#     # documents = loader.load_data(urls=['https://google.com'])
#     webpage = SimpleWebPageReader(html_to_text=True).load_data(
#         [url]
#     )
#     print(webpage[0].text)
#     return webpage


# # OP:beautiful soup get hardcode option

# #Ingestion pipeline section
# def semanticPipe(in_doc):
    
#     ## choose splitters

#     splitter = SemanticSplitterNodeParser(
#     buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
#     )
#     ## choose extractors
#     extractors = [
#     TitleExtractor(nodes=5, llm=llm),
#     QuestionsAnsweredExtractor(questions=3, llm=llm),
#     KeywordExtractor(keywords=10, llm=llm),
#     EntityExtractor(
#     prediction_threshold=0.5,
#     label_entities=False,  # include the entity label in the metadata
#     )]
    
#     #init pipe (extracts and they go into db)
#     pipeline = IngestionPipeline(transformations=[splitter]+extractors,
#     vector_store=semantic_vector_store)
#     #run pipe
#     nodes = pipeline.run(documents=in_doc)
#     for node in nodes:
#         print(f"Node: {node.text, node.metadata}\n\n")
#         print(node.metadata, '\n\n\n\n')
#         print(node.metadata.get('entities'), '\n\n\n\n')
#     return nodes

# #End Ingestion pipeline section




# ## set the structured output class
# class Scholarship(BaseModel):
#     """Object representing a single movie."""

#     name: str = Field(..., description="Name of the Scholarship.")
#     year: int = Field(..., description="Year of the Scholarship.")


# class Scholarships(BaseModel):
#     """Object representing a list of Scholarships."""

#     scholarships: List[Scholarship] = Field(..., description="List of scholarships.")



# testvars=['name','year']

# #Query pipeline section
# def queryPipe(website_name,vars):

#     output_parser = PydanticOutputParser(Scholarships)
#     json_prompt_str = """\
#     Please get the following variables about the {website_name} scholarship:
#     {get_vars}
#     Output with the following JSON format: 
#     """
#     json_prompt_str = output_parser.format(json_prompt_str)

#     json_prompt_tmpl = PromptTemplate(json_prompt_str)

#     p = QueryPipeline(chain=[json_prompt_tmpl, llm, output_parser], verbose=True)

#     ## this is where you put the variables in for the template
#     output = p.run(scholarship_name=website_name, get_vars=vars)
#     print(output)
#     #write json to file 


# #End Query pipeline section






# query_engine = index.as_query_engine()
# response = query_engine.query("What did the author do growing up?")
# display(response)
