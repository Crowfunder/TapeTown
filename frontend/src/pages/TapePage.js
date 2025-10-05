import React, { useState, useEffect } from 'react';
import './TapePage.css';
import ControlPanel from './ControlPanel';

export default function TapePage({ onBack, onAdd, onTapeSelect, onProfile, currentUserId }) {
  const [tapes, setTapes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTapes();
  }, []);

  const fetchTapes = async () => {
    try {
      setLoading(true);
      // Replace with your actual API endpoint
      const response = await fetch('YOUR_API_ENDPOINT_HERE');
      
      if (!response.ok) {
        throw new Error('Failed to fetch tapes');
      }
      
      const data = await response.json();
      setTapes(data);
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
          imageUrl: null
        },
        {
          id: 2,
          userName: 'Lorem Person',
          userAvatar: null,
          likes: 3000,
          title: 'Lorem ipsum',
          imageUrl: null
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

  const handleTapeClick = (tapeId) => {
    console.log('Tape clicked:', tapeId);
    if (onTapeSelect) {
      onTapeSelect(tapeId);
    }
  };

  const handleLike = (e, tapeId) => {
    e.stopPropagation(); // Prevent card click when liking
    console.log('Like tape:', tapeId);
    // Add like functionality here
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
    if (onProfile) {
      onProfile(); // Remove the hardcoded '1', let App.js handle the default
    }
  };

  const handleUserClick = (userId) => {
    if (onProfile) {
      onProfile(userId); // Just pass the userId, let App.js handle null cases
    }
  };

  const handleAvatarError = (e) => {
    e.target.src = 'fallback-avatar-url'; // Replace with your fallback avatar URL
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
            <div key={tape.id} className="tape-card" onClick={() => handleTapeClick(tape.id)}>
              {/* Tape Header */}
              <div className="tape-header">
                <div className="user-info" onClick={(e) => {
                  e.stopPropagation();
                  handleUserClick(tape.userId);
                }}>
                  <div className="user-avatar">
                    {tape.userAvatar ? (
                      <img src={tape.userAvatar} alt={tape.userName} onError={handleAvatarError} />
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

              {/* Tape Footer */}
              <div className="tape-footer">
                <div className="tape-stats">
                  <button className="like-button" onClick={(e) => handleLike(e, tape.id)}>
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