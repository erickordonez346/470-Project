from openai import OpenAI
from dotenv import dotenv_values
import os, json, time
from assistant import assistantExists, createAssistant, CavClone

environment_variables = dotenv_values()
openai_api_key = environment_variables["OPENAI_API_KEY"]

openai_client = OpenAI(api_key=openai_api_key)


message = "Based on the file zoom.txt, how many people submitted homework 3?"
my_clone = CavClone(openai_client)
print(f"{my_clone.send_message(message)}")
