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
import random
from datetime import datetime, timezone
from openai import OpenAI
from .response import assistantExists, createAssistant, CavClone
import elevenlabs
from elevenlabs import Voice, VoiceSettings, generate, play, set_api_key, save

# from audio import get_audio


environment_variables = dotenv_values()
openai_api_key = environment_variables["OPENAI_API_KEY"]
elevenlabs.set_api_key(environment_variables["ELEVEN_LABS_API_KEY"])

openai_client = OpenAI(api_key=openai_api_key)
clone = CavClone(openai_client)


# response from assistant
def get_response(query):
    return clone.send_message(query)


def get_audio(response):
    print("Generating audio...")
    audio = generate(
        text=response,
        voice=Voice(
            voice_id="O50T1e73qysLLp01btAR",
            settings=VoiceSettings(
                stability=0.88,
                similarity_boost=0.88,
                style=0.05,
                use_speaker_boost=True,
            ),
        ),
        model="eleven_multilingual_v2",
    )
    print("Audio Generation: completed")

    audio_num = "output_" + str(random.randint(0, 2147483648)) + ".mp3"
    save(audio, "chat/static/audio_files/" + audio_num)

    return audio_num


# <audio controls>
#                 <source src="cavclone/output.mp3" type="audio/mpeg">Testing!
#             </audio>


# -----------------------------------------PAGE VIEWS-----------------------------------------


def index(request):
    queries = Query.objects.all()
    form = QueryForm()

    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data["content"]
            # output = get_response(user_input)
            output = "no gpt"
            audio = get_audio(output)
            # audio = "/cavclone/output.mp3"
            print(audio)
            # output = "no gpt used"
            form = Query(content=user_input, response=output, audio_path=audio)
            form.save()

            # display clean
            form = QueryForm()
            return HttpResponseRedirect("chat")
        else:
            output = "no input! this is not expected to ever be hit"
    else:
        return render(
            request,
            "index.html",
            {
                "queries": queries,
                "form": form,
            },
        )
    return render(
        request,
        "index.html",
        {
            "queries": queries,
            "form": form,
            "output": output,
            "audio": audio,
        },
    )


def about(request):
    response = "Howdy! This is a project for CSCE 470: Information Storage and Retreival at Texas A&M University"
    return HttpResponse(response)


def record_activity(request):
    if request.method == "POST":
        Activity.objects.creat(enter_time=timezone.now())
        return JsonResponse({"status": "entered"})
    elif request.method == "PUT":
        activity = Activity.objects.filter(exit_time__isnull=True).last()
        if activity:
            activity.exit_time = timezone.now()
            activity.save()
            return JsonResponse({"status": "exited"})

    return HttpResponse(request)
