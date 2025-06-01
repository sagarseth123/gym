import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { adminSignup } from '../../services/api'; // Import the API service function
// import './AdminSignupPage.css';

const AdminSignupPage = () => {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setSuccessMessage('');

    // Basic validation (can be expanded)
    if (!fullName || !email || !password) {
      setError('All fields are required.');
      return;
    }

    try {
      // Use the adminSignup service function
      const data = await adminSignup({ fullName, email, password });
      setSuccessMessage(`Admin user ${data.email} created successfully! Redirecting to login...`);
      // Clear form fields
      setFullName('');
      setEmail('');
      setPassword('');
      setTimeout(() => {
        navigate('/login');
      }, 2000); // Redirect after 2 seconds
    } catch (error) {
      // Errors thrown by adminSignup service will have a 'message' property
      setError(error.message || 'An unexpected error occurred during signup.');
      console.error('Signup page error:', error);
    }
  };

  return (
    <div className="signup-page-container"> {/* Apply class for styling */}
      <h2>Admin Signup</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Full Name:
          <input
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
          />
        </label>
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
            minLength="8" // Basic password length validation
          />
        </label>
        <button type="submit">Sign Up</button>
      </form>
      {error && <p className="error-message">{error}</p>}
      {successMessage && <p className="success-message">{successMessage}</p>}
    </div>
  );
};

export default AdminSignupPage;
