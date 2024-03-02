import os
import json
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

loader = PyPDFLoader("test.pdf")
pages = loader.load_and_split()

db = Chroma.from_documents(pages, OpenAIEmbeddings())

query = "What skills do we have in this text?"
docs = db.similarity_search(query)
print(docs[0].page_content)


