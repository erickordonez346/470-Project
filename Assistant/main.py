from openai import OpenAI
from dotenv import dotenv_values

environment_variables = dotenv_values()
openai_api_key = environment_variables['OPENAI_API_KEY']

openai_client = OpenAI(api_key=openai_api_key)





