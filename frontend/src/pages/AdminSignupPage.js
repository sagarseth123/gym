// frontend/src/pages/AdminSignupPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { adminSignup } from '../services/api.js'; // Corrected path

const AdminSignupPage = () => {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');
    if (!fullName || !email || !password) {
      setError('All fields are required.');
      return;
    }
    // Basic password length validation (example)
    if (password.length < 8) {
        setError('Password must be at least 8 characters long.');
        return;
    }
    try {
      // The adminSignup service expects { fullName, email, password }
      const data = await adminSignup({ fullName, email, password });
      setSuccessMessage(`Admin user ${data.email} created successfully! Redirecting to login...`);
      // Clear form fields
      setFullName('');
      setEmail('');
      setPassword('');
      setTimeout(() => {
        navigate('/login');
      }, 2000); // Brief delay to show success message
    } catch (err) {
      setError(err.message || 'Failed to signup. Please try again.');
      console.error('Signup page error:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          {/* Optional: Placeholder for a logo */}
          {/* <img className="mx-auto h-12 w-auto" src="/path-to-logo.png" alt="AppName" /> */}
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create Admin Account
          </h2>
        </div>
        <form className="mt-8 space-y-6 bg-white p-10 shadow-xl rounded-lg" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="full-name" className="sr-only">Full name</label>
              <input
                id="full-name"
                name="fullName"
                type="text"
                autoComplete="name"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Full name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="email-address" className="sr-only">Email address</label>
              <input
                id="email-address"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" // No top/bottom border radius for middle elements
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Password (min. 8 characters)"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Sign up
            </button>
          </div>
          {error && (
            <p className="mt-4 text-center text-sm text-red-600 p-3 bg-red-100 rounded-md"> {/* Adjusted margin & added padding/bg */}
              {error}
            </p>
          )}
          {successMessage && (
            <p className="mt-4 text-center text-sm text-green-600 p-3 bg-green-100 rounded-md"> {/* Adjusted margin & added padding/bg */}
              {successMessage}
            </p>
          )}
        </form>
      </div>
    </div>
  );
};

export default AdminSignupPage;
