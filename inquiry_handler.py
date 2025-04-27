from openai import OpenAI
from sk import my_sk

client = OpenAI(api_key= my_sk)

class ChatBot():

    def __init__(self):
        self.thread_id, self.assistant_id = self.conversation_setup()

    def conversation_setup(self):

        # Create an assistant
        chat_assistant = client.beta.assistants.create(
            name = "Query assistant",
            model = 'gpt-4o',
            description = """A teaching assistant bot designed to help educators by categorizing their inquiries and performing the requested tasks."""
        )

        # Create a thread
        thread = client.beta.threads.create()

        # Add message to thread
        client.beta.threads.messages.create(
            thread_id = thread.id,
            role = "user",
            content = """The bot can summarize content, generate quizzes, grade responses, correct grammar and spelling, suggest creative projects, and draft emails. 
            It analyzes the user's input to determine the intended task and responds appropriately with a focused and helpful output."""
        )

        return thread.id, chat_assistant.id
    
    def chat_helper(self, prompt):

        # Add message
        client.beta.threads.messages.create(
            thread_id = self.thread_id,
            role = "user",
            content = prompt
        )

        # Run thread
        run = client.beta.threads.runs.create_and_poll(
             thread_id = self.thread_id,
            assistant_id = self.assistant_id,
            timeout = 1000
        )
        
        if run.status != "completed":
            raise Exception("Run failed:", run.status)
        
        # Create List of Messages
        message_cursor = client.beta.threads.messages.list(thread_id=self.thread_id)
        messages = [message for message in message_cursor]

        return messages[0].content[0].text.value


chatbot = ChatBot()

print(chatbot.chat_helper("Summarize the causes of the Cold War."))
print(chatbot.chat_helper("Create a 5-question quiz about photosynthesis."))
print(chatbot.chat_helper("Proofread this paragraph: 'Their going to the park tommorow.'"))
print(chatbot.chat_helper("Can you be more specific about the mistake"))