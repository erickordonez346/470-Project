import elevenlabs

# Generates voice
audio = elevenlabs.generate(
    text = "Hi we are creating a Caverlee Clone",
    voice = "Bella"
)

# Plays voice

elevenlabs.play(audio)