import React, { useState, useEffect } from 'react';
import './TapePage.css';
import ControlPanel from './ControlPanel';
import CONFIG from './Config';

export default function TapePage({ onBack, onAdd }) {
  const [tapes, setTapes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTapes();
  }, []);

  const fetchFileByHash = async (hash, type = 'image') => {
    try {
      const response = await fetch(`${CONFIG.API_URL.replace(/\/$/, '')}/files/${hash}`, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const blob = await response.blob();
      return URL.createObjectURL(blob);
    } catch (error) {
      console.error(`Error fetching ${type} file:`, error);
      return null;
    }
  };

  const fetchTapes = async () => {
    async function fetchRecommendedGuides(lat, lon, radiusKm = 10000, limit = 20) {
      const params = new URLSearchParams({
        latitude: lat,
        longitude: lon,
        radius_km: radiusKm,
        limit: limit,
      });

      const url = `${CONFIG.API_URL.replace(/\/$/, '')}/guides/recommended?${params.toString()}`;

      try {
        const response = await fetch(url, {
          method: 'GET',
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const guides = await response.json();
        return guides;

      } catch (error) {
        console.error('Error fetching recommended guides:', error);
        return [];
      }
    }

    try {
      setLoading(true);
      const guidesData = await fetchRecommendedGuides(55, 55); // hardcoded, to be pulled from user

      console.log('Guides data received:', guidesData);

      if (!guidesData || guidesData.length === 0) {
        console.log('No guides data received');
        setTapes([]);
        setLoading(false);
        return;
      }

      // Fetch images and audio for each tape
      const tapesWithMedia = await Promise.all(
        guidesData.map(async (tape) => {
          console.log('Processing tape:', tape);

          const imageUrl = tape.image_hash
            ? await fetchFileByHash(tape.image_hash, 'image')
            : null;

          return {
            id: tape.user_id || tape.id,
            userName: `User ${tape.user_id || tape.id}`,
            userAvatar: null,
            likes: tape.likes || 0,
            title: tape.name || 'Untitled',
            imageUrl: imageUrl,
            audioUrl: null,
            createdAt: tape.created_at
          };
        })
      );

      console.log('Tapes with media:', tapesWithMedia);
      setTapes(tapesWithMedia);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching tapes:', err);
      setError(err.message);
      setLoading(false);

      // Mock data for demonstration
      setTapes([
        {
          id: 1,
          userName: 'Lorem Person',
          userAvatar: null,
          likes: 3000,
          title: 'Lorem ipsum',
          imageUrl: null,
          audioUrl: null
        },
        {
          id: 2,
          userName: 'Lorem Person',
          userAvatar: null,
          likes: 3000,
          title: 'Lorem ipsum',
          imageUrl: null,
          audioUrl: null
        }
      ]);
    }
  };

  const handleBackClick = () => {
    console.log('Navigate back from tapes page');
    if (onBack) {
      onBack();
    }
  };

  const handleLike = (tapeId) => {
    console.log('Like tape:', tapeId);
    // Add like functionality here
  };

  const handleComment = (tapeId) => {
    console.log('Comment on tape:', tapeId);
    // Add comment functionality here
  };

  const handleShare = (tapeId) => {
    console.log('Share tape:', tapeId);
    // Add share functionality here
  };

  const handleMore = (tapeId) => {
    console.log('More options for tape:', tapeId);
    // Add more options functionality here
  };

  const handleHomeClick = () => {
    if (onBack) {
      onBack();
    }
  };

  const handleAddClick = () => {
    if (onAdd) {
      onAdd();
    }
  };

  const handleProfileClick = () => {
    console.log('Navigate to profile');
    // Add profile navigation logic here
  };

  if (loading) {
    return (
      <div className="tape-page">
        <div className="tape-container">
          <h1 className="tape-brand" onClick={handleHomeClick}>TAPE TOWN</h1>
          <div className="loading">Loading tapes...</div>
        </div>
        <ControlPanel
          onHome={handleHomeClick}
          onAdd={handleAddClick}
          onProfile={handleProfileClick}
          activePage="home"
        />
      </div>
    );
  }

  return (
    <div className="tape-page">
      <div className="tape-container">
        {/* Brand Title - clickable to go back */}
        <h1 className="tape-brand" onClick={handleBackClick}>TAPE TOWN</h1>

        {/* Tapes List */}
        <div className="tapes-list">
          {tapes.map((tape) => (
            <div key={tape.id} className="tape-card">
              {/* Tape Header */}
              <div className="tape-header">
                <div className="user-info">
                  <div className="user-avatar">
                    {tape.userAvatar ? (
                      <img src={tape.userAvatar} alt={tape.userName} />
                    ) : (
                      <div className="avatar-placeholder"></div>
                    )}
                  </div>
                  <span className="user-name">{tape.userName}</span>
                </div>
              </div>

              {/* Tape Image/Content */}
              <div className="tape-content">
                {tape.imageUrl ? (
                  <img src={tape.imageUrl} alt={tape.title} />
                ) : (
                  <div className="content-placeholder"></div>
                )}
              </div>

              {/* Audio Player */}
              {tape.audioUrl && (
                <div className="tape-audio">
                  <audio controls src={tape.audioUrl}>
                    Your browser does not support the audio element.
                  </audio>
                </div>
              )}

              {/* Tape Footer */}
              <div className="tape-footer">
                <div className="tape-stats">
                  <button className="like-button" onClick={() => handleLike(tape.id)}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                    </svg>
                    <span className="like-count">{tape.likes >= 1000 ? `${(tape.likes / 1000).toFixed(0)}k` : tape.likes}</span>
                  </button>
                </div>

                <h3 className="tape-title">{tape.title}</h3>
              </div>
            </div>
          ))}
        </div>
      </div>
      <ControlPanel 
        onHome={handleHomeClick}
        onAdd={handleAddClick}
        onProfile={handleProfileClick}
        activePage="home"
      />
    </div>
  );
}