from openai import OpenAI
from sk import my_sk
from openai.types.beta.threads.message_create_params import (
    Attachment,
    AttachmentToolFileSearch,
)

client = OpenAI(api_key= my_sk)

class DocBot:
    def __init__(self, file_name):
        self.file_name = [file_name]
        self.thread_id, self.pdf_assistant_id = self.conversation_setup()
    
    def conversation_setup(self):
        # Initializing Assistant
        pdf_assistant = client.beta.assistants.create(
        model = "gpt-4o",
        description = "Analyze the PDF document and answer any follow up questions.",
        tools = [
            {"type": "file_search"}
        ],
        name = "PDF assistant",
        )

        # Creating thread
        thread = client.beta.threads.create()

        # Upload file
        file = client.files.create(file = open(self.file_name[0],"rb"), purpose="assistants")

        # Create Assistant
        client.beta.threads.messages.create(
            thread_id = thread.id,
            role = "user",
            attachments = [
                Attachment(
                    file_id = file.id,
                    tools = [
                            AttachmentToolFileSearch(type="file_search")                
                    ]
                )
            ],

            content = """ Potential uses include: summarizing sections, grading answers, grammar checking text, 
            extracting key points, finding factual errors, or suggesting improvements.""",
        )

        return thread.id, pdf_assistant.id


    def doc_analyzer(self, prompt):

        # Add Message
        client.beta.threads.messages.create(
            thread_id = self.thread_id,
            role = "user",
            content = prompt,
        )

        # Run Thread
        run = client.beta.threads.runs.create_and_poll(
            thread_id = self.thread_id,
            assistant_id = self.pdf_assistant_id,
            timeout = 1000
        )

        if run.status != "completed":
            raise Exception("Run failed:", run.status)
    
        # Create List of Messages
        message_cursor = client.beta.threads.messages.list(thread_id=self.thread_id)
        messages = [message for message in message_cursor]


        return messages[0].content[0].text.value
    
    def add_doc(self, another_file):
        self.file_name.append(another_file)
        file = client.files.create(file = open(self.file_name[-1],"rb"), purpose="assistants")
        client.beta.threads.messages.create(
            thread_id = self.thread_id,
            role = "user",
            attachments = [
                Attachment(
                    file_id = file.id,
                    tools = [
                            AttachmentToolFileSearch(type="file_search")                
                    ]
                )
            ],
        content = "Analyze the PDF documents and answer any follow up questions."
        )


test_doc = DocBot("test2.pdf")
#print(test_doc.doc_analyzer("Who is the main character?"))
#print(test_doc.doc_analyzer("What genre is it?"))
#print(test_doc.doc_analyzer("When is this story set?"))
#print(test_doc.doc_analyzer("In terms of grammer, what would you give this paper out of 100?"))
print(test_doc.doc_analyzer("Summarize the story for me."))
test_doc.add_doc("RUBRIC.pdf")
test_doc.add_doc("test3.pdf")
print(test_doc.doc_analyzer("Now what happens in the story (with the added pdf)?"))
print(test_doc.doc_analyzer("Uisng the criteria in the rubric, give the student a score from 1 - 100"))
