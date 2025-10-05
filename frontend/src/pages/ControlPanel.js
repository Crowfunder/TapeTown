import React from 'react';
import './ControlPanel.css';

export default function ControlPanel({ onHome, onAdd, onProfile, activePage }) {
  const handleHomeClick = () => {
    console.log('Home button clicked');
    if (onHome) {
      onHome();
    }
  };

  const handleAddClick = () => {
    console.log('Add button clicked');
    if (onAdd) {
      onAdd();
    }
  };

  const handleProfileClick = () => {
    console.log('Profile button clicked');
    if (onProfile) {
      onProfile();
    }
  };

  return (
    <div className="control-panel">
      <div className="control-panel-container">
        <button 
          className={`control-btn ${activePage === 'home' ? 'active' : ''}`}
          onClick={handleHomeClick}
          title="Home"
        >
          <svg width="32" height="32" viewBox="0 0 32 32" fill="currentColor">
            <path d="M16 2.594l-13 11.594v15.812h9v-10h8v10h9v-15.812l-13-11.594zm0 3.375l9 8.031v12h-5v-10h-8v10h-5v-12l9-8.031z"/>
          </svg>
        </button>

        <button 
          className={`control-btn control-btn-primary ${activePage === 'add' ? 'active' : ''}`}
          onClick={handleAddClick}
          title="Add"
        >
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none" stroke="currentColor" strokeWidth="3">
            <line x1="20" y1="10" x2="20" y2="30"/>
            <line x1="10" y1="20" x2="30" y2="20"/>
          </svg>
        </button>

        <button 
          className={`control-btn ${activePage === 'profile' ? 'active' : ''}`}
          onClick={handleProfileClick}
          title="Profile"
        >
          <svg width="32" height="32" viewBox="0 0 32 32" fill="currentColor">
            <path d="M16 4c-3.314 0-6 2.686-6 6s2.686 6 6 6 6-2.686 6-6-2.686-6-6-6zm0 2c2.206 0 4 1.794 4 4s-1.794 4-4 4-4-1.794-4-4 1.794-4 4-4zm0 12c-4.418 0-8 1.791-8 4v4h16v-4c0-2.209-3.582-4-8-4zm0 2c3.513 0 6 1.194 6 2v2h-12v-2c0-0.806 2.487-2 6-2z"/>
          </svg>
        </button>
      </div>
    </div>
  );
}