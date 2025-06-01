import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { adminLogin } from '../services/api.js'; // Corrected import path
// Styles are assumed to be in App.css from previous step

const AdminLoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Email and password are required.');
      return;
    }

    try {
      // Use the adminLogin service function
      const data = await adminLogin({ email, password });
      if (data.access_token) {
        localStorage.setItem('authToken', data.access_token);
        // Optionally store token_type if your app uses it:
        // localStorage.setItem('tokenType', data.token_type);
        navigate('/admin/dashboard');
      } else {
        // This case should ideally not be reached if adminLogin throws an error on !response.ok
        // or if the backend guarantees access_token on successful login.
        // However, it's a safeguard.
        setError('Login successful, but no token received. Please contact support.');
      }
    } catch (error) {
      // Errors thrown by adminLogin service will have a 'message' property
      setError(error.message || 'An unexpected error occurred during login.');
      console.error('Login page error:', error);
    }
  };

  return (
    <div className="login-page-container"> {/* Apply class for styling */}
      <h2>Admin Login</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <button type="submit">Login</button>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default AdminLoginPage;
