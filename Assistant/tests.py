from openai import OpenAI
from dotenv import dotenv_values
import os, json, time
from assistant import assistantExists, createAssistant, CavClone

environment_variables = dotenv_values()
openai_api_key = environment_variables['OPENAI_API_KEY']

openai_client = OpenAI(api_key=openai_api_key)

# Test assistant api by walking through the following steps
# create assistant -> create thread -> create message -> run thread -> poll for response -> display response


# Test 1 without OOP 
##############################################################################################

my_assistant_id = ""
my_thread_id = ""

if not os.path.exists(os.path.join(os.getcwd(), "assistant.json")):
    with open("assistant.json", "w") as f:
        print(f"File created.")
        pass
# Set/Get assistant id
print(f"Retrieving assistant...")
if assistantExists(openai_client):
    with open("assistant.json", "r") as f:
        my_assistant_id = json.load(f)
    print(f"Assistant loaded from json file with id: {my_assistant_id}")
else:
    my_assistant_id = createAssistant(openai_client)
    print(f"Assistant created with id: {my_assistant_id}")

# Create Thread
print(f"Creating thread...")
thread = openai_client.beta.threads.create()
my_thread_id = thread.id
print(f"Thread created successfully with id: {my_thread_id}")

# Delete Thread
print(f"Deleting thread...")
response = openai_client.beta.threads.delete(my_thread_id)
print(f"Thread with id: {my_thread_id} deleted succesfully.")

################################################################################################

# Test 2 without OOP
################################################################################################

my_assistant_id = ""
my_thread_id = ""

if not os.path.exists(os.path.join(os.getcwd(), "assistant.json")):
    with open("assistant.json", "w") as f:
        print(f"File created.")
        pass
# Set/Get assistant id
print(f"Retrieving assistant...")
if assistantExists(openai_client):
    with open("assistant.json", "r") as f:
        my_assistant_id = json.load(f)
    print(f"Assistant loaded from json file with id: {my_assistant_id}")
else:
    my_assistant_id = createAssistant(openai_client)
    print(f"Assistant created with id: {my_assistant_id}")

# Create Thread
print(f"Creating thread...")
thread = openai_client.beta.threads.create()
my_thread_id = thread.id
print(f"Thread created successfully with id: {my_thread_id}")

message = "Howdy! What is 5 + 10?"

try:
    # Store message in thread so that assistant can answer
    print(f"Storing message...")
    message_object = openai_client.beta.threads.messages.create(
        my_thread_id,
        role="user",
        content=message 
    )
    print(f"Message Object: {message_object}")
    # Execute call in order for assistant to process and answer the message
    print(f"Message run started...")
    message_run = openai_client.beta.threads.runs.create(
        thread_id=my_thread_id,
        assistant_id=my_assistant_id
    )
    print(f"Message Run: {message_run}")
    run_id = message_run.id
    print("MESSAGE SENT")
    print("Waiting for assistant response...")

    # Poll for run status
    print(f"Polling for assistant response...")
    count = 0
    while(True):
        time.sleep(15)
        count = count + 1
        print(f"Attempt {count}...")
        run_status_response = openai_client.beta.threads.runs.retrieve(
            thread_id=my_thread_id,
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
  thread_id=my_thread_id
)
response_message = message_list.data[0].content[0].text.value
print(f"Message: {response_message}")

# Delete Thread
print(f"Deleting thread...")
response = openai_client.beta.threads.delete(my_thread_id)
print(f"Thread with id: {my_thread_id} deleted succesfully.")

##################################################################################################

# Test 3 with OOP
###################################################################################################

message = "Hello! Why is the pythagorean theorem important?"
my_clone = CavClone(openai_client)
print(f"{my_clone.send_message(message)}")




