import React, { useState, useRef } from 'react';
import './RecordPage.css';
import ControlPanel from './ControlPanel';

export default function RecordPage({ onBack, onSave, onProfile }) {
  const [isRecording, setIsRecording] = useState(false);
  const [title, setTitle] = useState('');
  const [coverImage, setCoverImage] = useState(null);
  const [coverPreview, setCoverPreview] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const handleCoverSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setCoverImage(file);
      const reader = new FileReader();
      reader.onload = (e) => setCoverPreview(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      console.error('Error accessing microphone:', err);
      alert('Could not access microphone');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        audioChunksRef.current = [audioBlob];
      };
      setIsRecording(false);
    }
  };

  const handleSave = async () => {
    if (!title) {
      alert('Please enter a title');
      return;
    }

    const formData = new FormData();
    formData.append('title', title);
    if (coverImage) {
      formData.append('image', coverImage);
    }
    if (audioChunksRef.current.length > 0) {
      formData.append('audio', audioChunksRef.current[0]);
    }

    try {
      const response = await fetch('/api/guides/upload', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) throw new Error('Upload failed');
      onSave();
    } catch (err) {
      console.error('Error saving tape:', err);
      alert('Failed to save tape');
    }
  };

  return (
    <div className="record-page">
      <div className="record-container">
        <h1 className="record-brand">TAPE TOWN</h1>

        <div className="record-card">
          <div className="user-info">
            <div className="user-avatar">
              <div className="avatar-placeholder"></div>
            </div>
            <span className="user-name">Lorem Person</span>
          </div>

          <div className="tape-section">
            <input
              type="text"
              className="title-input"
              placeholder="Your title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <div className="tape-wheels">
              <div className="wheel"></div>
              <div className="wheel"></div>
            </div>
            <button 
              className={`record-button ${isRecording ? 'recording' : ''}`}
              onClick={isRecording ? stopRecording : startRecording}
            >
              {isRecording ? (
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <rect x="6" y="4" width="4" height="16"/>
                  <rect x="14" y="4" width="4" height="16"/>
                </svg>
              ) : (
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <circle cx="12" cy="12" r="8"/>
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>
      <ControlPanel 
        onHome={onBack}
        onAdd={() => {}} // Disabled since we're already on record page
        onProfile={onProfile} // Added onProfile handler
        activePage="add"
      />
    </div>
  );
}

