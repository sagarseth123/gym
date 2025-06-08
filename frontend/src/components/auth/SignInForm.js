// frontend/src/components/auth/SignInForm.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { adminLogin } from '../../services/api.js'; // Adjusted path for components/auth directory

const SignInForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!email || !password) {
      setError('Email and password are required.');
      return;
    }
    try {
      const data = await adminLogin({ email, password });
      if (data.access_token) {
        localStorage.setItem('authToken', data.access_token);
        navigate('/admin/dashboard');
      } else {
        // This case might indicate an unexpected response structure even on success
        // or if adminLogin service doesn't throw an error for some reason.
        setError('Login successful, but no token received. Please contact support.');
      }
    } catch (err) {
      setError(err.message || 'Failed to login. Please check your credentials.');
      console.error('Sign In form error:', err);
    }
  };

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      <div>
        <label htmlFor="signin-email" className="sr-only">Email address</label>
        <input
          id="signin-email"
          name="email"
          type="email"
          autoComplete="email"
          required
          className="appearance-none block w-full px-3 py-3 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Email address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      <div>
        <label htmlFor="signin-password" className="sr-only">Password</label>
        <input
          id="signin-password"
          name="password"
          type="password"
          autoComplete="current-password"
          required
          className="appearance-none block w-full px-3 py-3 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      {/* Optional: Remember me / Forgot password could go here if needed */}

      <div>
        <button
          type="submit"
          className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-600"
        >
          Sign In
        </button>
      </div>
      {error && (
        <p className="mt-4 text-center text-sm text-red-600 p-3 bg-red-100 rounded-md"> {/* Consistent error styling */}
          {error}
        </p>
      )}
    </form>
  );
};

export default SignInForm;
