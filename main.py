from flask import Flask, request, send_file
import zipfile
import os
import tempfile
import json
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from openai import OpenAI

app = Flask(__name__)


@app.route('/')
def index():

    file = request.files['resumeFile']

    if file:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Save the uploaded file to the temporary directory
        tempFilePath = os.path.join(temp_dir, file.filename)
        file.save(tempFilePath)

        # Process the file if needed
        # For demonstration, let's just print the temporary file path


        zipBuffer = zipfile.ZipFile('site.zip', 'w', zipfile.ZIP_DEFLATED)

        # Modify the 'index.html' content as needed
        generatedIndexFile = generateIndexFile(tempFilePath)

        # Add the modified 'index.html' content to the ZIP archive
        zipBuffer.writestr('index.html', generatedIndexFile)

        # Walk through the 'template' directory and add all other files and directories
        for root, dirs, files in os.walk('template'):
            for file in files:
                if file != 'index.html':
                    file_path = os.path.join(root, file)
                    zipBuffer.write(file_path, os.path.relpath(file_path, 'template'))
        zipBuffer.close()
        return send_file('site.zip', as_attachment=True)


# Function to generate the 'index.html' file
def generateIndexFile(resumeFile):
    indexContent = ""
    # read in the index.html file template
    with open('template/index.html', 'r') as f:
        indexContent = f.read()

    load_dotenv()

    loader = PyPDFLoader(resumeFile)
    pages = loader.load_and_split()

    db = Chroma.from_documents(pages, OpenAIEmbeddings())

    query = " "
    docs = db.similarity_search(query)
    print(docs[0].page_content)

    openAiClient = OpenAI()

    # about me section
    aboutMeResponse = openAiClient.chat.completions.create(
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
    aboutMeJson = json.loads(aboutMeResponse.choices[0].message.content)

    indexContent = indexContent.replace("{{aboutme}}", aboutMeJson['aboutMe'])

    # list jobs

    jobsHtml = """"""

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
    listJobsJson = json.loads(listJobs.choices[0].message.content)

    for job in listJobsJson['jobs']:

        jobHtmlTemplate = """
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
        jobsHtml += jobHtmlTemplate.replace("Project Title", job['title']).replace("Company Name", job['company']).replace("description here", job['description'])

    indexContent = indexContent.replace("{{jobs}}", jobsHtml)

    # list skills
    skillsTemplate = "<h1 class=\"dark-blue-text\">type</h1>"
    skillsHtml = """"""




if __name__ == '__main__':
    app.run(debug=True)