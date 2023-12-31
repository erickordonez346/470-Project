import time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import QueryForm
from .models import Query
from dotenv import dotenv_values
import random
from openai import OpenAI
from .response import CavClone
import elevenlabs
from elevenlabs import Voice, VoiceSettings, generate, save, stream


environment_variables = dotenv_values()
openai_api_key = environment_variables["OPENAI_API_KEY"]
elevenlabs.set_api_key(environment_variables["ELEVEN_LABS_API_KEY"])

openai_client = OpenAI(api_key=openai_api_key)

clone = CavClone(openai_client)


# response from assistant
def get_response(query):
    return clone.send_message(query)


def get_audio(response):
    print("Streaming Audio")
    audio_stream = generate(
        text=response,
        voice=Voice(
        voice_id="O50T1e73qysLLp01btAR",
        settings=VoiceSettings(
            stability=0.88, similarity_boost=0.88, style=0.05, use_speaker_boost=True
            ),
        ),
        model="eleven_multilingual_v2",
        stream=True
    )
    stream(audio_stream)
    print("Finished Streaming Audio")
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


# -----------------------------------------PAGE VIEWS-----------------------------------------


def index(request):
    queries = Query.objects.all()
    form = QueryForm()

    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data["content"]
            output = get_response(user_input)
            audio = get_audio(output)
            # output = "no gpt"
            # audio = "output_2067994949.mp3"
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
