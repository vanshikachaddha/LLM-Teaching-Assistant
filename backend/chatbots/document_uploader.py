from openai import OpenAI
from openai.types.beta.threads.message_create_params import (
    Attachment,
    AttachmentToolFileSearch,
)
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class DocBot:
    def __init__(self, file_names: list[str]):
        self.file_names = file_names
        self.thread_id, self.pdf_assistant_id = self.conversation_setup()

    def conversation_setup(self):
        # Initialize Assistant
        pdf_assistant = client.beta.assistants.create(
            model="gpt-4o",
            description="Analyze the uploaded documents and answer follow-up questions.",
            tools=[{"type": "file_search"}],
            name="PDF Assistant",
        )

        # Create Thread
        thread = client.beta.threads.create()

        # Upload files and prepare attachments
        attachments = []
        for fname in self.file_names:
            file_path = os.path.join("documents", fname)
            file = client.files.create(file=open(file_path, "rb"), purpose="assistants")
            attachments.append(
                Attachment(
                    file_id=file.id,
                    tools=[AttachmentToolFileSearch(type="file_search")]
                )
            )

        # Initial message with all attachments
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            attachments=attachments,
            content="""These documents may be used for summarizing, grading, fact-checking, or providing feedback. 
            Please review them carefully for any follow-up questions."""
        )

        return thread.id, pdf_assistant.id

    def doc_analyzer(self, prompt):
        # Add message to thread
        client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=prompt,
        )

        # Run thread
        run = client.beta.threads.runs.create_and_poll(
            thread_id=self.thread_id,
            assistant_id=self.pdf_assistant_id,
            timeout=1000
        )

        if run.status != "completed":
            raise Exception("Run failed:", run.status)

        # Get latest message
        message_cursor = client.beta.threads.messages.list(thread_id=self.thread_id)
        messages = [msg for msg in message_cursor]
        return messages[0].content[0].text.value

    def add_doc(self, another_file: str):
        self.file_names.append(another_file)
        file_path = os.path.join("documents", another_file)
        file = client.files.create(file=open(file_path, "rb"), purpose="assistants")
        client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            attachments=[
                Attachment(
                    file_id=file.id,
                    tools=[AttachmentToolFileSearch(type="file_search")]
                )
            ],
            content="New document added. Please incorporate this into your understanding for future questions."
        )