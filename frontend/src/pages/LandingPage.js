import React from 'react';
import './LandingPage.css';

export default function LandingPage({ onLogin, onRegister, onTapesClick }) {
  const handleLoginClick = () => {
    console.log('Login button clicked in LandingPage');
    if (onLogin) {
      onLogin();
    } else {
      console.error('onLogin prop is not defined');
    }
  };

  const handleRegisterClick = () => {
    console.log('Register button clicked in LandingPage');
    if (onRegister) {
      onRegister();
    } else {
      console.error('onRegister prop is not defined');
    }
  };

  const handleTapesClick = (e) => {
    e.preventDefault();
    console.log('TAPE TOWN title clicked in LandingPage');
    console.log('onTapesClick prop:', onTapesClick);
    if (onTapesClick) {
      console.log('Calling onTapesClick...');
      onTapesClick();
    } else {
      console.error('onTapesClick prop is not defined');
    }
  };

  return (
    <div className="landing-page">
      {/* Logo Section */}
      <div className="logo-section">
        <div className="logo-container">
          {/* Card with logo */}
          <div className="logo-card">
            {/* Logo icon placeholder */}
            <div className="logo-icon">
              <svg width="120" height="120" viewBox="0 0 120 120">
                <path d="M30 40 L50 40 L50 80 L30 80 Z M70 40 L90 40 L90 80 L70 80 Z" 
                      fill="currentColor" opacity="0.8"/>
                <circle cx="40" cy="95" r="12" fill="currentColor"/>
                <circle cx="80" cy="95" r="12" fill="currentColor"/>
              </svg>
            </div>
          </div>
          {/* Small logo on top */}
          <div className="logo-badge">
            <svg width="40" height="40" viewBox="0 0 40 40">
              <circle cx="15" cy="20" r="6" fill="white"/>
              <circle cx="25" cy="20" r="6" fill="white"/>
            </svg>
          </div>
        </div>

        {/* Title */}
        <h1 className="main-title clickable-title" onClick={handleTapesClick}>
          TAPE TOWN
        </h1>

        {/* Subtitle */}
        <h2 className="subtitle">Social travelling platform</h2>

        {/* Description */}
        <p className="description">
          Explore the tapes recorded by guides and users all around the world! Experience the beautiful by learning the meaningful context.
        </p>
      </div>

      {/* Bottom Section with gradient background */}
      <div className="cta-section">
        <p className="cta-label">Calm the city experience</p>
        
        <h3 className="cta-title">
          Any town,<br/>anywhere
        </h3>

        {/* Buttons */}
        <div className="button-group">
          <button className="btn btn-primary" onClick={handleLoginClick}>
            Log in
          </button>
          <button className="btn btn-secondary" onClick={handleRegisterClick}>
            Register
          </button>
        </div>
      </div>

      {/* Bottom spacing */}
      <div className="bottom-spacer"></div>
    </div>
  );
}