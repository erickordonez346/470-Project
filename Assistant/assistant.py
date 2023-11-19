from openai import OpenAI
import os, time, json

# Effectively creates a thread for the user to communicate with the assistant
class CavClone():
    def __init__(self, client: OpenAI) -> None:
        self.client = client
        self.assistant_id = ""
        self.thread_id = ""

        if not os.path.exists(os.path.join(os.getcwd(), "assistant.json")):
            with open("assistant.json", "w") as f:
                print(f"File created.")
                pass
        # Set/Get assistant id
        print(f"Retrieving assistant...")
        if assistantExists(openai_client):
            with open("assistant.json", "r") as f:
                self.assistant_id = json.load(f)
            print(f"Assistant loaded from json file with id: {self.assistant_id}")
        else:
            self.assistant_id = createAssistant(openai_client)
            print(f"Assistant created with id: {self.assistant_id}")

        # Create thread
        print(f"Creating thread...")
        openai_client = self.client
        thread = openai_client.beta.threads.create()
        self.thread_id = thread.id
        print(f"Thread created successfully with id: {self.thread_id}")

    def send_message(self, message: str) -> str:
        openai_client = self.client
        try:
            # Store message in thread so that assistant can answer
            print(f"Storing message...")
            message_object = openai_client.beta.threads.messages.create(
                self.thread_id,
                role="user",
                content=message 
            )
            # Execute call in order for assistant to process and answer the message
            print(f"Message run started...")
            message_run = openai_client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id
            )
            run_id = message_run.id
            print("MESSAGE SENT")
            print("Waiting for assistant response...")

            # Poll for run status
            print(f"Polling for assistant response...")
            run_status_response = openai_client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run_id
            )

            count = 0
            while(True):
                time.sleep(15)
                count = count + 1
                print(f"Attempt {count}...")
                run_status_response = openai_client.beta.threads.runs.retrieve(
                    thread_id=self.thread_id,
                    run_id=run_id
                )
                print(f"Run Status Response: {run_status_response.status}")
                if run_status_response.status == "completed":
                    print(f"Response detected.")
                    break

        except Exception as e:
            print("MESSAGE FAILED TO SEND")
            print("Error Details:")
            print(f"{e}")

        # Display response to the console
        message_list = openai_client.beta.threads.messages.list(
        thread_id=self.thread_id
        )
        response_message = message_list.data[0].content[0].text.value
        print(f"Message: {response_message}")

    def __del__(self) -> None:
        # Delete Thread (May need to be changed later for simplification)
        print(f"Deleting thread...")
        openai_client = self.client
        response = openai_client.beta.threads.delete(self.thread_id)
        print(f"Thread with id: {self.thread_idthread_id} deleted succesfully.")



# Function to create an OpenAI Assistant
def createAssistant(openai_client: OpenAI) -> str:
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
def assistantExists(openai_client: OpenAI) -> bool:
    my_assistant = ""
    try:
        if os.path.exists(os.path.join(os.getcwd(), "assistant.json")):
            with open("assistant.json", "r") as f:
                id = json.load(f)
        my_assistant = openai_client.beta.assistants.retrieve(id)
    except Exception as e:
        my_assistant = "Not Found"

    if my_assistant != "Not Found" and my_assistant != "":
        return True
    else:
        return False
