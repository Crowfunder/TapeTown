import React, { useState, useEffect, useRef } from 'react';
import './TapeDetailsPage.css';
import ControlPanel from './ControlPanel';

export default function TapeDetailsPage({ tapeId, onBack, onAdd, onProfile }) {
  const [tape, setTape] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);

  useEffect(() => {
    if (tapeId) {
      fetchTapeDetails();
    }
  }, [tapeId]); // Remove fetchTapeDetails from deps as it's defined in component

  const fetchTapeDetails = async () => {
    try {
      setLoading(true);
      // Replace with your actual API endpoint
      const response = await fetch(`YOUR_API_ENDPOINT/tapes/${tapeId}`);
      if (!response.ok) throw new Error('Failed to fetch tape details');
      const data = await response.json();
      setTape(data);
    } catch (err) {
      console.error('Error:', err);
      // Mock data for demonstration
      setTape({
        id: tapeId,
        userName: 'Lorem Person',
        userAvatar: null,
        likes: 3000,
        title: 'Lorem ipsum',
        imageUrl: null,
        audioUrl: 'sample-audio.mp3',
        description: 'Detailed description of the tape...',
        latitude: 52.2297,  // Changed from location
        longitude: 21.0122, // Added longitude
        createdAt: '2024-03-15'
      });
    } finally {
      setLoading(false);
    }
  };

  const handlePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleAddClick = () => {
    if (onAdd) {
      onAdd();
    }
  };

  const handleProfileClick = () => {
    if (onProfile) {
      onProfile();
    }
  };

  if (loading || !tape) {
    return (
      <div className="tape-details-page">
        <div className="loading">Loading...</div>
        <ControlPanel 
          onHome={onBack}
          onAdd={handleAddClick}
          onProfile={handleProfileClick}
          activePage="details"
        />
      </div>
    );
  }

  return (
    <div className="tape-details-page">
      <div className="tape-details-container">
        {/* Header */}
        <div className="details-header">
          <button className="back-button" onClick={onBack}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
            </svg>
          </button>
          <h1 className="details-title">{tape.title}</h1>
        </div>

        {/* Main Content */}
        <div className="details-content">
          {/* User Info */}
          <div className="details-user-info">
            <div className="user-avatar">
              {tape.userAvatar ? (
                <img src={tape.userAvatar} alt={tape.userName} />
              ) : (
                <div className="avatar-placeholder"></div>
              )}
            </div>
            <span className="user-name">{tape.userName}</span>
          </div>
          
          <div className="details-image">
            {tape.imageUrl ? (
              <img src={tape.imageUrl} alt={tape.title} />
            ) : (
              <div className="image-placeholder" />
            )}
          </div>

          {/* Audio Player */}
          <div className="audio-player">
            <div className="tape-wheels">
              <div className="wheel"></div>
              <div className="wheel"></div>
            </div>
            <audio ref={audioRef} src={tape.audioUrl} />
            <button className={`play-button ${isPlaying ? 'playing' : ''}`} onClick={handlePlayPause}>
              {isPlaying ? (
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <rect x="6" y="4" width="4" height="16"/>
                  <rect x="14" y="4" width="4" height="16"/>
                </svg>
              ) : (
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <polygon points="5,3 19,12 5,21"/>
                </svg>
              )}
            </button>
          </div>

          {/* Metadata */}
          <div className="details-metadata">
            <div className="metadata-row">
              <span className="metadata-label">Coordinates:</span>
              <span className="metadata-value">
                {tape.latitude?.toFixed(4)}°N, {tape.longitude?.toFixed(4)}°E
              </span>
            </div>
          </div>

          {/* Description */}
          <p className="details-description">{tape.description}</p>
        </div>
      </div>
      <ControlPanel 
        onHome={onBack}
        onAdd={handleAddClick}
        onProfile={handleProfileClick}
        activePage="details"
      />
    </div>
  );
}
