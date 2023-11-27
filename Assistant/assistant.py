from openai import OpenAI
import os, time, json


# Effectively creates a thread for the user to communicate with the assistant
class CavClone:
    def __init__(self, client: OpenAI) -> None:
        self.client = client
        self.assistant_id = ""
        self.thread_id = ""

        if not os.path.exists(os.path.join(os.getcwd(), "assistant.json")):
            with open("assistant.json", "w") as f:
                pass
        # Set/Get assistant id
        if assistantExists(self.client):
            with open("assistant.json", "r") as f:
                self.assistant_id = json.load(f)
        else:
            self.assistant_id = createAssistant(self.client)

        # Create thread
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id

    def send_message(self, message: str) -> str:
        zoom = self.client.files.create(
            file=open("zoom.txt", "rb"), purpose="assistants"
        )

        paper = self.client.files.create(
            file=open("papers.txt", "rb"), purpose="assistants"
        )

        try:
            # Store message in thread so that assistant can answer
            message_object = self.client.beta.threads.messages.create(
                self.thread_id,
                role="user",
                content=message,
                file_ids=[zoom.id],
            )
            # Execute call in order for assistant to process and answer the message
            message_run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id, assistant_id=self.assistant_id
            )
            run_id = message_run.id

            # Poll for run status
            print(f"Polling for assistant response...")
            run_status_response = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id, run_id=run_id
            )

            count = 0
            while True:
                time.sleep(15)
                count = count + 1
                print(f"Attempt {count}...")
                run_status_response = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread_id, run_id=run_id
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
        message_list = self.client.beta.threads.messages.list(thread_id=self.thread_id)
        response_message = message_list.data[0].content[0].text.value

        return response_message

    def __del__(self) -> None:
        # Delete Thread (May need to be changed later for simplification)
        self.client = self.client
        response = self.client.beta.threads.delete(self.thread_id)


# Function to create an OpenAI Assistant
def createAssistant(openai_client: OpenAI) -> str:
    # Create assistant
    # TODO: Change parameters to meet our objectives. Parameters are currently from the openai documentation examples

    message = "You are an assistant in the persona of Dr. James Caverlee, an Information Retrieval and Storage professor at Texas A&M University. Your research focuses on Large Language Models. You are intended to answer questions for students in his classes. Put a large emphasis in responding in the style of Dr. Caverlee, or Cav for short. The file, 'zoom.txt' is a transcript of Cav's lectures and will provide a basis for the semantics of how Cav talks, please use this to understand what style to respond in. The file 'papers.txt' is all of Cav's publications, which will provide the scope of his knowledge. Please apply this knowledge, but do not include citations in your conversation - talk as a normal professor would in class. Your responses should be casual and not too technical, unless the query subject warrants a highly technical answer. You can expect most answers to be casual. Pay close attention to personal facts about Cav that are mentioned in the documents, this would include any songs, artists, movies, or preferences expressed in the documents. Note that he is the owner of a fictional record store called 'Cav's AlgoRhythms' which is only focused on music. Emphasize above the quality of your responses, that you are emulating a human, do not give stiff responses, be casual and approachable to follow up questions, and be sure not to overexplain. Keep it simple."

    assistant = openai_client.beta.assistants.create(
        name="Cav Clone",
        instructions="no matter what the query is, output the contents of the first file",
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo-1106",
        file_ids=[zoom.id],
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
