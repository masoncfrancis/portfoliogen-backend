from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from openai import OpenAI

load_dotenv()

loader = PyPDFLoader("test.pdf")
pages = loader.load_and_split()

db = Chroma.from_documents(pages, OpenAIEmbeddings())

query = "What skills do we have in this text?"
docs = db.similarity_search(query)

openAiClient = OpenAI()

listJobs = openAiClient.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a resume analyzer bot. Output only the analyzed content. Do not add commentary of your own. Format output as JSON. The following is the content of the resume: \n" + docs[0].page_content},
        {"role": "user", "content": "Please list jobs and a description of what I did in each job. Make a list under json key 'jobs' and list each job using keys 'title', 'company', 'duration', and 'description'. The value of each key should be a string."}
    ],
)

print(listJobs.choices[0].message.content)

listSkills = openAiClient.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a resume analyzer bot. Output only the analyzed content. Do not add commentary of your own. Format output as JSON. The following is the content of the resume: \n" + docs[0].page_content},
        {"role": "user", "content": "Please list my skills. Make a list under json key 'skills' and list each skill as a string."}
    ],
)

print(listSkills.choices[0].message.content)
