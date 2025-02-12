import React, { useState, useRef } from "react"
import axios from "axios"

const AudioRecorder = () => {
  const [recording, setRecording] = useState(false)
  const [transcription, setTranscription] = useState("")
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const recorder = new MediaRecorder(stream)

      recorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data)
      }

      recorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/mp3" })
        await uploadAudio(audioBlob)
        audioChunksRef.current = []
      }

      recorder.start()
      mediaRecorderRef.current = recorder
      setRecording(true)
    } catch (error) {
      console.error("Error accessing microphone:", error)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop()
      setRecording(false)
    }
  }

  const uploadAudio = async (blob: Blob) => {
    const formData = new FormData()
    formData.append("file", blob, "audio.mp3")

    try {
      const response = await axios.post<{ text: string }>(
        "http://127.0.0.1:5000/transcribe", 
        formData, 
        {
          headers: { "Content-Type": "multipart/form-data" },
          withCredentials: false,
        }
      )
      setTranscription(response.data.text)
    } catch (error) {
      console.error("Error:", error)
    }
  }

  return (
    <div>
      <button onClick={recording ? stopRecording : startRecording}>
        {recording ? "Stop Recording" : "Start Recording"}
      </button>
      {transcription && <p>Transcription: {transcription}</p>}
    </div>
  )
}

export default AudioRecorder 