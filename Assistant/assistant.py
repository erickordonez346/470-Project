import json
import os

# Effectively creates a thread for the user to communicate with the assistant
class CavClone():
    def __init__(self, client):
        self.client = client
        self.assistant_id = ""

        # TODO: Test if this creates a new json file in the cwd
        if not os.path.exists(os.path.join(os.getcwd(), "assistant.json")):
            with open("assistant.json", "w"):
                pass
        # Set/Get assistant id
        if assistantExists(openai_client):
            with open("assistant.json", "r") as f:
                self.assistant_id = json.load(f)
        else:
            self.assistant_id = createAssistant(openai_client)

        # Create thread
        openai_client = self.client
        thread = openai_client.beta.threads.create()
        self.thread_id = thread.id

    def send_message(self, message):
        openai_client = self.client
        try:
            message_object = openai_client.beta.threads.messages.create(
                self.thread_id,
                role="user",
                conten=message 
            )
            message_run = openai_client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id
            )
            run_id = message_run.id
            print("MESSAGE SENT")
            print("Waiting for assistant response...")

            # TODO: Poll for run status and return response once completed or an error if one occurs

        except Exception as e:
            print("MESSAGE FAILED TO SEND")
            print("Error Details:")
            print(f"{e}")

    def __del__(self):
        # Delete Thread (May need to be changed later for simplification)
        openai_client = self.client
        response = openai_client.beta.threads.delete(self.thread_id)



# Function to create an OpenAI Assistant
def createAssistant(openai_client):
    # Create assistant
    # TODO: Change parameters to meet our objectives. Parameters are currently from the openai documentation examples
    assistant = openai_client.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a personal math tutor. Write and run code to answer math questions.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo-1106"
    )

    # Store Assistant ID in json file
    with open("assistant.json", "w") as f:
        json.dump(assistant.id, f)

    return assistant.id
    
# Function that returns boolean value indicating whether or not an assistant already exists
def assistantExists(openai_client):
    my_assistant = ""
    try:
        my_assistant = openai_client.beta.assistants.retrieve("asst_abc123")
    except Exception as e:
        my_assistant = "Not Found"

    if my_assistant != "Not Found" and my_assistant != "":
        return True
    else:
        return False
