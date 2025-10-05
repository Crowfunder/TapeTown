import React, { useState } from 'react';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import TapePage from './pages/TapePage';
import TapeDetailsPage from './pages/TapeDetailsPage';
import RecordPage from './pages/RecordPage';
import ProfilePage from './pages/ProfilePage';

export default function App() {
  const [currentPage, setCurrentPage] = useState('landing');
  const [selectedTapeId, setSelectedTapeId] = useState(null);
  const [selectedUserId, setSelectedUserId] = useState(null);
  const [currentUserId, setCurrentUserId] = useState(null); // Add this line for logged in user

  const navigateToLogin = () => {
    console.log('Navigating to login');
    setCurrentPage('login');
  };

  const navigateToRegister = () => {
    console.log('Navigating to register');
    setCurrentPage('register');
  };

  const navigateToLanding = () => {
    console.log('Navigating to landing');
    setCurrentPage('landing');
  };

  const navigateToTapes = () => {
    console.log('Navigating to tapes');
    setCurrentPage('tapes');
  };

  const navigateToAdd = () => {
    console.log('Navigating to record page');
    setCurrentPage('record');
  };

  // Update the profile navigation to handle both self and other profiles
  const navigateToProfile = (userId = null) => {
    console.log('Navigating to profile:', userId || currentUserId);
    setSelectedUserId(userId || currentUserId || '1'); // Use currentUserId as fallback before '1'
    setCurrentPage('profile');
  };

  const navigateToTapeDetails = (tapeId) => {
    console.log('Navigating to tape details:', tapeId);
    setSelectedTapeId(tapeId);
    setCurrentPage('tapeDetails');
  };

  console.log('Current page:', currentPage);

  if (currentPage === 'login') {
    return (
      <LoginPage 
        onBack={navigateToLanding}
        onRegister={navigateToRegister}
      />
    );
  }

  if (currentPage === 'register') {
    return (
      <RegisterPage 
        onBack={navigateToLanding}
        onLogin={navigateToLogin}
      />
    );
  }

  if (currentPage === 'tapes') {
    return (
      <TapePage 
        onBack={navigateToLanding}
        onTapeSelect={navigateToTapeDetails}
        onAdd={navigateToAdd}
        onProfile={navigateToProfile}
        currentUserId={currentUserId}
      />
    );
  }

  if (currentPage === 'tapeDetails') {
    return (
      <TapeDetailsPage 
        tapeId={selectedTapeId}
        onBack={() => setCurrentPage('tapes')}
        onAdd={navigateToAdd}
        onProfile={navigateToProfile}
        currentUserId={currentUserId}
      />
    );
  }

  if (currentPage === 'record') {
    return (
      <RecordPage 
        onBack={() => setCurrentPage('tapes')}
        onSave={() => setCurrentPage('tapes')}
        onProfile={navigateToProfile} // Added onProfile handler
        currentUserId={currentUserId}
      />
    );
  }

  if (currentPage === 'profile') {
    return (
      <ProfilePage 
        userId={selectedUserId}
        onBack={() => setCurrentPage('tapes')}
        onAdd={navigateToAdd}
        onTapeSelect={navigateToTapeDetails}
      />
    );
  }

  return (
    <LandingPage 
      onLogin={navigateToLogin}
      onRegister={navigateToRegister}
      onTapesClick={navigateToTapes}
    />
  );
}