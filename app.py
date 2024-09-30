from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
from gtts import gTTS
import os
import subprocess
import traceback  # For detailed error messages
from datetime import date 


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from tts import generate_voiceover
from screen_recorder import start_recording

app = Flask(__name__)

# Set up the folder for saving MP3 files
OUTPUT_FOLDER = 'voiceover'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/generate_script', methods=['POST'])
def generate_script():
    try:
        data = request.get_json()  # Retrieve JSON data from the request
        software_name = data.get('software_name')
        os_type = data.get('os_type')
        lang = data.get('lang')

        # Check if the required parameters are present
        if not software_name or not os_type:
            return jsonify({"error": "Missing required parameters"}), 400

        # Generate today's date
        today_date = date.today().isoformat()
        prompt = f"Generate a step-by-step installation guide in {lang} language, " \
                  f"in inline-html format without html, doctype and head tags, " \
                  f"for {software_name} on {os_type}, " \
                  f"start with a guide title in html H1, here is the english example title 'How to Install {software_name} on {os_type} step by step guide - {today_date}.'"

        # Call OpenAI API to generate the script
        response = client.chat.completions.create(  # Ensure you are using the correct method for your model
            model="gpt-4o-mini",  # Ensure you're using the correct model
            messages=[
                {"role": "system", "content": "You are a helpful software and devops engineer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        installation_script = response.choices[0].message.content  # Extract the generated script
        return jsonify({"script": installation_script})  # Return the generated script

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/gen_voice', methods=['POST'])
def gen_voice():
    data = request.get_json()  # Get the JSON payload
    text = data.get('text')
    langv = data.get('langv')
    is_slow = data.get('is_slow')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        tts = gTTS(text, lang=langv, slow=is_slow)
        output_file = os.path.join(app.config['OUTPUT_FOLDER'], 'output.mp3')
        tts.save(output_file)
        return jsonify({"mp3file": output_file})
    except Exception as e:
        return jsonify({"error": str(e)}), 500







# Record video function
def start_recording(os_type):
    if os_type == 'macOS':
        command = "ffmpeg -f avfoundation -framerate 30 -i 1 -r 30 -y output_macOS.mp4"
    elif os_type == 'Windows':
        command = "ffmpeg -f gdigrab -framerate 30 -i desktop -y output_windows.mp4"
    elif os_type == 'Ubuntu':
        command = "ffmpeg -f x11grab -framerate 30 -i :0.0 -y output_ubuntu.mp4"
    else:
        return None

    # Run the command and check for errors
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")  # Print the error message
        return None

    return f"output_{os_type}.mp4"

@app.route('/record_screen', methods=['POST'])
def record_screen():
    try:
        # Parse JSON data
        data = request.get_json()

        # Check if 'os_type' is present in the JSON
        if not data or 'os_type' not in data:
            return jsonify({"error": "Invalid request, 'os_type' missing"}), 400

        os_type = data['os_type']
        output_file = start_recording(os_type)

        # Return response based on recording status
        if output_file:
            return jsonify({"output_file": output_file}), 200
        else:
            return jsonify({"error": "Recording failed"}), 500
    except Exception as e:
        # Return detailed error message
        print(traceback.format_exc())  # Print the stack trace
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
