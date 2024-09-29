from gtts import gTTS

def generate_voiceover(text, output_file="voiceover.mp3"):
    tts = gTTS(text)
    output_path = os.path.join(app.config['voiceover'], 'voiceover.mp3')
    tts.save(output_file)
    return output_file
