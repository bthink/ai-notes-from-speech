import os
import whisper
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydub import AudioSegment
import functions_framework

# Path to Firebase service account key
service_account_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")

# Initialize Firebase (only if not already initialized)
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)
    
db = firestore.client()

app = Flask(__name__)
CORS(app)
# Load Whisper model
model = whisper.load_model("small")

@functions_framework.http
def transcribe_audio(request):
    try:
        if request.method != "POST":
            return jsonify({"error": "Invalid request method"}), 405

        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        # Save uploaded audio
        audio_file = request.files["file"]
        audio_path = "/tmp/temp_audio.mp3"  # Use /tmp for Firebase functions

        audio_file.save(audio_path)

        # Convert to MP3 if needed
        if audio_file.filename.endswith(".wav"):
            audio = AudioSegment.from_wav(audio_path)
            audio.export(audio_path, format="mp3")

        # Transcribe using Whisper
        result = model.transcribe(audio_path, language="pl")
        os.remove(audio_path)  # Cleanup temp file

        # Store in Firestore
        doc_ref = db.collection("transcriptions").add({
            "text": result["text"],
            "timestamp": firestore.SERVER_TIMESTAMP
        })

        return jsonify({"id": doc_ref[1].id, "text": result["text"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
