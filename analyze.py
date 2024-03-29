from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from openai import OpenAI

load_dotenv()

loader = PyPDFLoader("test2.pdf")
pages = loader.load_and_split()

db = Chroma.from_documents(pages, OpenAIEmbeddings())

query = " "
docs = db.similarity_search(query)
print(docs[0].page_content)

openAiClient = OpenAI()

aboutMe = openAiClient.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system",
         "content": "You are a resume analyzer bot. Format output as JSON. The following is the content of the resume: \n" +
                    docs[0].page_content},
        {"role": "user",
         "content": "Get the about me section for the user and return it under the key 'aboutMe'. The value should be a string. If there is an about me statement given, give it without changes. If there is no about me statement available, make a generalized one based off of the resume content. Do not mention previous work or volunteer experience."}
    ],
)

print(aboutMe.choices[0].message.content)

listJobs = openAiClient.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system",
         "content": "You are a resume analyzer bot. Format output as JSON. The following is the content of the resume: \n" +
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
         "content": "You are a resume analyzer bot. Format output as JSON. The following is the content of the resume: \n" +
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
         "content": "You are a resume analyzer bot. Format output as JSON. The following is the content of the resume: \n" +
                    docs[0].page_content},
        {"role": "user",
         "content": "Make a list under json key 'projects' and list each project using keys 'title', 'company', and 'description'. The value of each key should be a string."}
    ],
)

print(listProjects.choices[0].message.content)

listURLs = openAiClient.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system",
         "content": "You are a resume analyzer bot. Format output as JSON. The following is the content of the resume: \n" +
                    docs[0].page_content},
        {"role": "user",
         "content": "Check for URLS for LinkedIn and GitHub. For keys 'linkedin' and 'github' in the JSON, the applicable URL should be set as the value, and should be a fully formatted URL. If no URL is found, the value should be set to null."}
    ],
)

print(listURLs.choices[0].message.content)
