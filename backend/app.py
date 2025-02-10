from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load Whisper model
model = whisper.load_model("small")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # Save uploaded audio
    audio_file = request.files["file"]
    audio_path = "temp_audio.mp3"
    audio_file.save(audio_path)

    # Convert to MP3 if needed
    if audio_file.filename.endswith(".wav"):
        audio = AudioSegment.from_wav(audio_path)
        audio.export(audio_path, format="mp3")

    # Transcribe using Whisper
    result = model.transcribe(audio_path, language="pl")
    os.remove(audio_path)  # Cleanup temp file

    return jsonify({"text": result["text"]})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
