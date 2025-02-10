import React, { useState } from "react";
import axios from "axios";

const AudioRecorder = () => {
  const [recording, setRecording] = useState(false);
  const [transcription, setTranscription] = useState("");
  const [mediaRecorder, setMediaRecorder] = useState(null);  // Store mediaRecorder state
  let audioChunks = [];

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream); // Create recorder instance

    recorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    recorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/mp3" });
      await uploadAudio(audioBlob);
    };

    recorder.start();
    setMediaRecorder(recorder);  // Save to state
    setRecording(true);
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();  // Now `mediaRecorder` is correctly defined
      setRecording(false);
    }
  };

  const uploadAudio = async (blob) => {
    const formData = new FormData();
    formData.append("file", blob, "audio.mp3");

    try {
      const response = await axios.post("http://127.0.0.1:5000/transcribe", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        withCredentials: false, // Ensures no cross-origin cookies interfere
      });
      setTranscription(response.data.text);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <button onClick={recording ? stopRecording : startRecording}>
        {recording ? "Stop Recording" : "Start Recording"}
      </button>
      {transcription && <p>Transcription: {transcription}</p>}
    </div>
  );
};

export default AudioRecorder;
