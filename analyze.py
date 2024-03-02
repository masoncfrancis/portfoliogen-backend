from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from openai import OpenAI

load_dotenv()

loader = PyPDFLoader("test.pdf")
pages = loader.load_and_split()

db = Chroma.from_documents(pages, OpenAIEmbeddings())

query = " "
docs = db.similarity_search(query)
print(docs[0].page_content)

openAiClient = OpenAI()

listJobs = openAiClient.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system",
         "content": "You are a resume analyzer bot. Output only the analyzed content. Do not add commentary of your own. Format output as JSON. The following is the content of the resume: \n" +
                    docs[0].page_content},
        {"role": "user",
         "content": "Make a list under json key 'jobs' and list each job using keys 'title', 'company', 'duration', and 'description'. The value of each key should be a string."}
    ],
)

print(listJobs.choices[0].message.content)

listSkills = openAiClient.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system",
         "content": "You are a resume analyzer bot. Output only the analyzed content. Do not add commentary of your own. Format output as JSON. The following is the content of the resume: \n" +
                    docs[0].page_content},
        {"role": "user", "content": "Make a list under json key 'skills' and list each skill as a string."}
    ],
)

print(listSkills.choices[0].message.content)

projectFormatting = """
          <article class="rowproj">
            <div class="project-wrapper__text">
              <h3 class="project-wrapper__text-title">Project Title</h3>
              <h4 class="project-wrapper__text-title">Company Name</h4>
              <p class="project-wrapper__text-info">
                description here
              </p>
            </div>
          </article>
"""

listProjects = openAiClient.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system",
         "content": "You are a resume analyzer bot. Output only the analyzed content. Do not add commentary of your own. Format output as JSON. The following is the content of the resume: \n" +
                    docs[0].page_content},
        {"role": "user",
         "content": "Make a list under json key 'projects' and list each project using keys 'title', 'company', and 'description'. The value of each key should be a string."}
    ],
)

print(listProjects.choices[0].message.content)
