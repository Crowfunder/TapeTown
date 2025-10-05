import React, { useState, useEffect } from 'react';
import './ProfilePage.css';
import ControlPanel from './ControlPanel';

export default function ProfilePage({ userId, onBack, onAdd, onTapeSelect }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, [userId]);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      // Replace with actual API endpoint
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) throw new Error('Failed to fetch profile');
      const data = await response.json();
      setProfile(data);
    } catch (err) {
      console.error('Error:', err);
      // Mock data
      setProfile({
        username: 'Bob Destroyer',
        avatar: null,
        description: 'A little paragraph introduction that gives a sense of what you do, who you are, where you\'re from, and why you created this website. This is the most likely part of the page to be read in full.',
        tapes: [
          {
            id: 1,
            title: 'Lorem ipsum',
            likes: 3000,
            imageUrl: null
          },
          // ...more tapes
        ]
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="profile-page loading">Loading...</div>;
  }

  return (
    <div className="profile-page">
      <div className="profile-container">
        <div className="profile-header">
          <h1 className="profile-brand">TAPE TOWN</h1>
        </div>

        <div className="profile-card">
          <div className="profile-info">
            <div className="profile-avatar">
              {profile.avatar ? (
                <img src={profile.avatar} alt={profile.username} />
              ) : (
                <div className="avatar-placeholder">
                  {/* Simple illustration placeholder */}
                  <svg width="64" height="64" viewBox="0 0 64 64" fill="#9ca3af">
                    <path d="M32 0c17.7 0 32 14.3 32 32S49.7 64 32 64 0 49.7 0 32 14.3 0 32 0zm0 10c-5.5 0-10 4.5-10 10s4.5 10 10 10 10-4.5 10-10-4.5-10-10-10zm0 24c-8.3 0-16 4.1-16 8v4h32v-4c0-3.9-7.7-8-16-8z"/>
                  </svg>
                </div>
              )}
            </div>
            <h2 className="profile-name">{profile.username}</h2>
            <p className="profile-description">{profile.description}</p>
          </div>

          <div className="profile-tapes">
            {profile.tapes.map(tape => (
              <div key={tape.id} className="profile-tape-card" onClick={() => onTapeSelect(tape.id)}>
                <div className="tape-image">
                  {tape.imageUrl ? (
                    <img src={tape.imageUrl} alt={tape.title} />
                  ) : (
                    <div className="image-placeholder" />
                  )}
                </div>
                <div className="tape-info">
                  <h3 className="tape-title">{tape.title}</h3>
                  <span className="tape-likes">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                    </svg>
                    {tape.likes >= 1000 ? `${(tape.likes / 1000).toFixed(0)}k` : tape.likes}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      <ControlPanel 
        onHome={onBack}
        onAdd={onAdd}
        activePage="profile"
      />
    </div>
  );
}
    
