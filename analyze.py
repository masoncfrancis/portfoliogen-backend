import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from langchain.vectorstores.chroma import Chroma

load_dotenv()

llm = ChatOpenAI()

loader = UnstructuredHTMLLoader(os.getenv("LINKEDIN_PROFILE_URL"))
docs = loader.load()

htmlSplitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.HTML, chunk_size=60, chunk_overlap=0
)
htmlDocs = htmlSplitter.create_documents([docs])

print(htmlDocs)
