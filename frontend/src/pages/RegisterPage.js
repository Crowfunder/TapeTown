import React, { useState } from 'react';
import './RegisterPage.css';

export default function RegisterPage({ onBack, onLogin }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    mobileNumber: '',
    password: '',
    confirmPassword: '',
    agreeTerms: false
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Registration attempt with:', formData);
    
    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }
    
    if (!formData.agreeTerms) {
      alert('Please agree to the terms and conditions');
      return;
    }
    
    // Add your registration logic here
    alert('Registration successful!');
  };

  const handleLoginClick = () => {
    console.log('Navigate to login from register page');
    if (onLogin) {
      onLogin();
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        {/* Brand Title */}
        <h1 className="register-brand">TAPE TOWN</h1>

        {/* Register Header */}
        <h2 className="register-heading">Register</h2>
        <p className="register-description">
          Enter your details to register
        </p>

        {/* Register Form */}
        <form className="register-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="text"
              name="name"
              placeholder="Name"
              value={formData.name}
              onChange={handleChange}
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <input
              type="email"
              name="email"
              placeholder="Email Address"
              value={formData.email}
              onChange={handleChange}
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <div className="mobile-input-wrapper">
              <div className="country-code">
                <span className="flag">🇿🇦</span>
                <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
                  <path d="M6 8L2 4h8L6 8z"/>
                </svg>
              </div>
              <input
                type="tel"
                name="mobileNumber"
                placeholder="Mobile Number"
                value={formData.mobileNumber}
                onChange={handleChange}
                className="form-input mobile-input"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <input
              type="password"
              name="confirmPassword"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
              onChange={handleChange}
              className="form-input"
              required
            />
          </div>

          {/* Terms Checkbox */}
          <div className="terms-group">
            <input
              type="checkbox"
              id="agreeTerms"
              name="agreeTerms"
              checked={formData.agreeTerms}
              onChange={handleChange}
              className="terms-checkbox"
              required
            />
            <label htmlFor="agreeTerms" className="terms-label">
              I agree with the <a href="#" className="terms-link">terms and conditions</a>
            </label>
          </div>

          <button type="submit" className="btn-register">
            Next
          </button>
        </form>

        {/* Help Center */}
        <p className="help-text">
          Need help? Visit our <a href="#" className="help-link">help center</a>
        </p>
      </div>
    </div>
  );
}