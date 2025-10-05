import React, { useState } from 'react';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import TapePage from './pages/TapePage';

export default function App() {
  const [currentPage, setCurrentPage] = useState('landing');

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
    console.log('Navigating to add');
    setCurrentPage('add');
    // You'll create this page later
  };

  const navigateToProfile = () => {
    console.log('Navigating to profile');
    setCurrentPage('profile');
    // You'll create this page later
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