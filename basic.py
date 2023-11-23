import json
import re
import textwrap
import json
import logging
import http.client
import os
from datetime import datetime

# 11 Labs Imports and Setting API Key
import elevenlabs
from elevenlabs import Voice, VoiceSettings, generate, play, set_api_key

elevenlabs.set_api_key('183cf9ac1aac0a221c24d1115336fdc4')

# Set your API key
api_key = "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"

#### INFORMATION GATHERING HELPER FUNCTIONS ####
query = input("Ask Cav a Question: ")

PROMPT = (
    "Return a response to the following question in the character of Ted Lasso:\n"
    + str(query)
)

ENGINE = "text-davinci-003"

MAX_TOKENS = 2048


def openai_query(prompt=PROMPT, temperature=0.19, max_tokens=MAX_TOKENS, engine=ENGINE):
    data = {
        "model": engine,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    endpoint_url = "api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {openai_api_key}".format(openai_api_key=api_key),
    }
    connection = http.client.HTTPSConnection("api.openai.com")
    print(connection)
    json_req_data = json.dumps(data)
    connection.request("POST", "/v1/completions", json_req_data, headers)
    connection_response = connection.getresponse()
    print(connection_response)
    response_data = connection_response.read()
    connection.close()
    parsed_data = json.loads(response_data)
    logging.info("OpenAI request succeeded!")
    logging.info("Response: {data}".format(data=parsed_data))
    return parsed_data


def format_response(api_response, max_width=80):
    # Split the response into sentences
    sentences = re.split("(?<=[.!?]) +", api_response)

    # Initialize the formatted response string
    formatted_response = ""

    # Iterate through the sentences, wrapping and adding them to the formatted response
    for sentence in sentences:
        wrapped_sentence = textwrap.fill(sentence, width=max_width)
        formatted_response += wrapped_sentence + "\n\n"

    return "\n" + formatted_response.strip() + "\n"


response = openai_query()
result_text = response["choices"][0]["text"]

# Calling 11 Labs Cav Voice
audio = generate(
    text= result_text,
    voice=Voice(
        voice_id='O50T1e73qysLLp01btAR',
        settings=VoiceSettings(stability=0.88, similarity_boost=0.88, style=0.05, use_speaker_boost=True)
    ),
    model="eleven_multilingual_v2"
)

play(audio)

# result_text = "didn't run chatGPT"
print("Prompt:\n\n" + PROMPT)
print(result_text)

# write results to file
with open("results.txt", "w") as file:
    file.write("Run at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    file.write(result_text)
    file.write("\n\n---------------------------\n\n")
