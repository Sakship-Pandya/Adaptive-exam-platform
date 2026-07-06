import React, { useState } from 'react';
import './Auth.css';

export default function Auth() {
  const [isSignUp, setIsSignUp] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    rememberMe: false
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [successState, setSuccessState] = useState(null); // 'login' | 'signup' | null
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    // Clear errors for that field
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (isSignUp) {
      if (!formData.username.trim()) {
        newErrors.username = 'Username is required';
      } else if (formData.username.trim().length < 3) {
        newErrors.username = 'Username must be at least 3 characters';
      }
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email or Username is required';
    } else if (isSignUp || formData.email.includes('@')) {
      // Perform email check if signing up, or if user is logging in using an email structure
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(formData.email)) {
        newErrors.email = 'Please enter a valid email address';
      }
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (isSignUp) {
      if (!formData.confirmPassword) {
        newErrors.confirmPassword = 'Please confirm your password';
      } else if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = 'Passwords do not match';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    // Simulate backend response
    setTimeout(() => {
      setIsLoading(false);
      if (isSignUp) {
        setSuccessState('signup');
      } else {
        setSuccessState('login');
      }
    }, 1200);
  };

  const handleToggleMode = (signUpMode) => {
    setIsSignUp(signUpMode);
    setErrors({});
    setFormData({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      rememberMe: false
    });
  };

  const resetAuth = () => {
    setSuccessState(null);
    setFormData({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      rememberMe: false
    });
  };

  // Mock icons used inside the layout
  const UserIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
  );

  const MailIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
  );

  const LockIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
  );

  const EyeIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
  );

  const EyeOffIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.52 13.52 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" x2="22" y1="2" y2="22"/></svg>
  );

  return (
    <div className="auth-page">
      <div className="auth-wrapper">
        


        {/* RIGHT SIDE: AUTHENTICATION FORMS OR SUCCESS splash SCREEN */}
        <div className="auth-form-container">
          
          {successState ? (
            /* Successful sign-in or sign-up redirect screen */
            <div className="auth-success-screen">
              <div className="auth-success-circle">✓</div>
              <h2 className="auth-success-title">
                {successState === 'signup' ? 'Account Created!' : 'Welcome Back!'}
              </h2>
              <p className="auth-success-text">
                {successState === 'signup' 
                  ? `Hey ${formData.username || 'Aryan'}, your account has been successfully set up. Get ready to tackle your study goals!`
                  : `Good evening, ${formData.email.split('@')[0] || 'Aryan'}! Prepare to dive into your interactive studies.`
                }
              </p>
              <button className="auth-success-btn" onClick={resetAuth}>
                Proceed to Dashboard
              </button>
            </div>
          ) : (
            <>
              {/* Tab options for switching Login / Sign Up */}
              <div className="auth-tab-bar">
                <button 
                  className={`auth-tab-button ${!isSignUp ? 'active' : ''}`}
                  onClick={() => handleToggleMode(false)}
                >
                  Sign In
                </button>
                <button 
                  className={`auth-tab-button ${isSignUp ? 'active' : ''}`}
                  onClick={() => handleToggleMode(true)}
                >
                  Create Account
                </button>
              </div>

              {/* Form header details */}
              <div className="auth-form-header" key={isSignUp ? 'signup' : 'login'}>
                <h1 className="auth-form-title">
                  {isSignUp ? 'Create Account' : 'Welcome Back'}
                </h1>
                <p className="auth-form-subtitle">
                  {isSignUp 
                    ? 'Fill in your details to start preparing for exams' 
                    : 'Access your spaces, streaks, and practice quizzes'
                  }
                </p>
              </div>

              {/* Form Validation Global Error Messages */}
              {Object.keys(errors).length > 0 && !isSignUp && (
                <div className="auth-alert auth-alert-error">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
                  <span>Please check your entry and try again.</span>
                </div>
              )}

              {/* Form element */}
              <form className="auth-form" onSubmit={handleSubmit} noValidate>
                
                {/* Username Input (Only on Sign Up) */}
                <div className={`auth-field-transition ${isSignUp ? 'expanded' : 'collapsed'}`}>
                  <div className="auth-input-group">
                    <label className="auth-input-label" htmlFor="username">Username</label>
                    <div className="auth-input-wrapper">
                      <span className="auth-input-icon"><UserIcon /></span>
                      <input
                        type="text"
                        name="username"
                        id="username"
                        placeholder="e.g. aryan_patel"
                        className="auth-input"
                        value={formData.username}
                        onChange={handleInputChange}
                        tabIndex={isSignUp ? 0 : -1}
                      />
                    </div>
                    {errors.username && <span className="auth-alert-error" style={{ fontSize: '11px', marginTop: '2px', padding: '2px 8px', borderRadius: '4px' }}>{errors.username}</span>}
                  </div>
                </div>

                {/* Email Address Input */}
                <div className="auth-input-group">
                  <label className="auth-input-label" htmlFor="email">
                    {isSignUp ? 'Email Address' : 'Email or Username'}
                  </label>
                  <div className="auth-input-wrapper">
                    <span className="auth-input-icon"><MailIcon /></span>
                    <input
                      type="email"
                      name="email"
                      id="email"
                      placeholder={isSignUp ? "username@example.com" : "Enter email or username"}
                      className="auth-input"
                      value={formData.email}
                      onChange={handleInputChange}
                    />
                  </div>
                  {errors.email && <span className="auth-alert-error" style={{ fontSize: '11px', marginTop: '2px', padding: '2px 8px', borderRadius: '4px' }}>{errors.email}</span>}
                </div>

                {/* Password Input */}
                <div className="auth-input-group">
                  <label className="auth-input-label" htmlFor="password">
                    {isSignUp ? 'Create Password' : 'Password'}
                  </label>
                  <div className="auth-input-wrapper">
                    <span className="auth-input-icon"><LockIcon /></span>
                    <input
                      type={showPassword ? "text" : "password"}
                      name="password"
                      id="password"
                      placeholder="••••••••"
                      className="auth-input auth-input-password-padding"
                      value={formData.password}
                      onChange={handleInputChange}
                    />
                    <button
                      type="button"
                      className="auth-password-toggle"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? <EyeOffIcon /> : <EyeIcon />}
                    </button>
                  </div>
                  {errors.password && <span className="auth-alert-error" style={{ fontSize: '11px', marginTop: '2px', padding: '2px 8px', borderRadius: '4px' }}>{errors.password}</span>}
                </div>

                {/* Confirm Password Input (Only on Sign Up) */}
                <div className={`auth-field-transition ${isSignUp ? 'expanded' : 'collapsed'}`}>
                  <div className="auth-input-group">
                    <label className="auth-input-label" htmlFor="confirmPassword">Confirm Password</label>
                    <div className="auth-input-wrapper">
                      <span className="auth-input-icon"><LockIcon /></span>
                      <input
                        type={showConfirmPassword ? "text" : "password"}
                        name="confirmPassword"
                        id="confirmPassword"
                        placeholder="••••••••"
                        className="auth-input auth-input-password-padding"
                        value={formData.confirmPassword}
                        onChange={handleInputChange}
                        tabIndex={isSignUp ? 0 : -1}
                      />
                      <button
                        type="button"
                        className="auth-password-toggle"
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        tabIndex={isSignUp ? 0 : -1}
                      >
                        {showConfirmPassword ? <EyeOffIcon /> : <EyeIcon />}
                      </button>
                    </div>
                    {errors.confirmPassword && <span className="auth-alert-error" style={{ fontSize: '11px', marginTop: '2px', padding: '2px 8px', borderRadius: '4px' }}>{errors.confirmPassword}</span>}
                  </div>
                </div>

                {/* Extra Options: Remember Me & Forgot Password (Only on Login) */}
                <div className={`auth-field-transition ${!isSignUp ? 'expanded' : 'collapsed'}`}>
                  <div className="auth-extra-options">
                    <label className="auth-remember-me">
                      <input
                        type="checkbox"
                        name="rememberMe"
                        className="auth-checkbox"
                        checked={formData.rememberMe}
                        onChange={handleInputChange}
                        tabIndex={!isSignUp ? 0 : -1}
                      />
                      Remember me
                    </label>
                    <a href="#forgot" className="auth-forgot-link" onClick={(e) => e.preventDefault()} tabIndex={!isSignUp ? 0 : -1}>
                      Forgot Password?
                    </a>
                  </div>
                </div>

                {/* Submit Action Button */}
                <button type="submit" className="auth-submit-btn" disabled={isLoading} key={isSignUp ? 'signup-btn' : 'login-btn'}>
                  {isLoading ? (
                    <span className="auth-btn-spinner"></span>
                  ) : (
                    <span>{isSignUp ? 'Create Account' : 'Sign In'}</span>
                  )}
                </button>

              </form>
            </>
          )}
        </div>

      </div>
    </div>
  );
}
