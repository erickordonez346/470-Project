from django.shortcuts import render
from django.http import HttpResponse
from .forms import QueryForm
from .models import Query
import json
import re
import textwrap
import json
import logging
import http.client
import os
from datetime import datetime

api_key = "apikey"

ENGINE = "text-davinci-003"

MAX_TOKENS = 2048

output = ""


def query(userinput):
    PROMPT = (
        "Return a response to the following question in the character of Ted Lasso:\n"
        + str(userinput)
    )
    response = openai_query(PROMPT)
    result_text = response["choices"][0]["text"]
    return result_text
    # result_text = "didn't run chatGPT"
    # print("Prompt:\n\n" + PROMPT)
    # print(result_text)

    # # write results to file
    # with open("results.txt", "w") as file:
    #     file.write("Run at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    #     file.write(result_text)
    #     file.write("\n\n---------------------------\n\n")


def openai_query(prompt, temperature=0.19, max_tokens=MAX_TOKENS, engine=ENGINE):
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


def index(request):
    queries = Query.objects.all()
    form = QueryForm()

    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data["content"]
            # output = query(user_input)
            output = "no gpt used"
            form = Query(content=user_input, response=output)
            form.save()

            # display clean
            form = QueryForm()
        else:
            output = "no input! this is not expected to ever be hit"
    else:
        return render(request, "index.html", {"queries": queries, "form": form})
    return render(
        request, "index.html", {"queries": queries, "form": form, "output": output}
    )


def about(request):
    response = "Howdy! This is a project for CSCE 470: Information Storage and Retreival at Texas A&M University"
    return HttpResponse(response)
