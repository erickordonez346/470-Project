import time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import QueryForm
from .models import Query, Activity
from dotenv import dotenv_values
import json
import re
import textwrap
import json
import logging
import http.client
import os
from datetime import datetime, timezone
import elevenlabs
from elevenlabs import Voice, VoiceSettings, generate, play, set_api_key, save

# API Key that has Cav Voice, try not to use it too much as it's not unlimited
environment_variables = dotenv_values()
elevenlabs.set_api_key(environment_variables["ELEVEN_LABS_API_KEY"])

# Set your API key
api_key = environment_variables["OPENAI_API_KEY"]

#### INFORMATION GATHERING HELPER FUNCTIONS ####
result_text = response["choices"][0]["text"]

# Calling 11 Labs Cav Voice
audio = generate(
    text=result_text,
    voice=Voice(
        voice_id="O50T1e73qysLLp01btAR",
        settings=VoiceSettings(
            stability=0.88, similarity_boost=0.88, style=0.05, use_speaker_boost=True
        ),
    ),
    model="eleven_multilingual_v2",
)

save(audio, "output.mp3")
