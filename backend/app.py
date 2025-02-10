from flask import Flask, request, jsonify
import whisper
import os
from pydub import AudioSegment

app = Flask(__name__)

# Load Whisper model (adjust model size for performance)
model = whisper.load_model("small")  # Change to "base", "medium", etc.

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
    result = model.transcribe(audio_path, language="pl")  # Force Polish transcription
    os.remove(audio_path)  # Cleanup temp file

    return jsonify({"text": result["text"]})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
