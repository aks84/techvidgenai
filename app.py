from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
from gtts import gTTS
import os


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from tts import generate_voiceover
from screen_recorder import start_recording

app = Flask(__name__)

# Set up the folder for saving MP3 files
OUTPUT_FOLDER = 'voiceover'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Load OpenAI API key from environment variable

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_script', methods=['POST'])
def generate_script():
    try:
        software_name = request.form.get('software_name')
        os_type = request.form.get('os_type')
        
        # Check if the required parameters are present
        if not software_name or not os_type:
            return jsonify({"error": "Missing required parameters"}), 400

        # Prompt for script generation
        prompt = f"Generate a step-by-step installation guide, in inline-html format without html, doctype and head tags, for {software_name} on {os_type}, start with in html H1 'How to Install software_name on os_type step by step guide - 'today\'s date'."

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Ensure you're using the correct model
            messages=[
                {"role": "system", "content": "You are a helpful software installation engineer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        # print("Audio Script generated...")

        installation_script = response.choices[0].message.content
        return jsonify({"script": installation_script})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/gen_voice', methods=['POST'])
def gen_voice():
    data = request.get_json()  # Get the JSON payload
    text = data.get('text')
    lang = data.get('lang')
    is_slow = data.get('is_slow')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        tts = gTTS(text, lang=lang, slow=is_slow)
        output_file = os.path.join(app.config['OUTPUT_FOLDER'], 'output.mp3')
        tts.save(output_file)
        return jsonify({"mp3file": output_file})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/record_screen', methods=['POST'])
def record_screen():
    os_type = request.form.get('os_type')
    output_file = start_recording(os_type)
    return jsonify({"output_file": output_file})


if __name__ == '__main__':
    app.run(debug=True)

