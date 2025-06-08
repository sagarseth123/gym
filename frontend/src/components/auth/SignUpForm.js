// frontend/src/components/auth/SignUpForm.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { adminSignup } from '../../services/api.js'; // Adjusted path

const SignUpForm = () => {
  const [fullName, setFullName] = useState('');
  const [roleType, setRoleType] = useState('user'); // Default to 'user'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');

    if (!fullName || !email || !password || !roleType) {
      setError('All fields are required.');
      return;
    }
    if (password.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }

    try {
      // For now, roleType from dropdown is not sent to backend via adminSignup,
      // as current backend endpoint /auth/signup/admin creates an admin.
      // The adminSignup service function takes { fullName, email, password }.
      const data = await adminSignup({ fullName, email, password });
      setSuccessMessage(`Admin account for ${data.email} created successfully! Please sign in.`);
      setFullName('');
      setRoleType('user'); // Reset dropdown to default
      setEmail('');
      setPassword('');
      setTimeout(() => {
        // Navigate to the AuthPage, which defaults to showing SignInForm,
        // or explicitly navigate to a path that shows the sign-in form if AuthPage structure changes.
        // For now, '/auth' seems to be intended to show AuthPage with its default state (signin tab).
        // To ensure signin tab is active, we might need to pass state or have AuthPage default to signin.
        // The current AuthPage defaults to 'signin' tab, so '/auth' should work if AuthPage is at '/auth'.
        // Assuming /auth is the route for AuthPage which then shows AuthCard.
        // If AuthPage itself isn't at /auth, this navigation might need adjustment.
        // For now, let's assume /auth will land on AuthPage, which will default to signin tab.
        // A more robust way would be for AuthPage to accept a prop to set initial tab,
        // or for navigate to set a state that AuthPage reads.
        // For this task, navigate('/auth') and relying on AuthPage's default is acceptable.
        // Or, more directly, if '/login' is the sign-in specific route:
        navigate('/login'); // Direct to login page
      }, 2500);
    } catch (err) {
      setError(err.message || 'Failed to sign up. Please try again.');
      console.error('Sign Up form error:', err);
    }
  };

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      <div>
        <label htmlFor="signup-fullname" className="sr-only">Full Name</label>
        <input
          id="signup-fullname"
          name="fullName"
          type="text"
          autoComplete="name"
          required
          className="appearance-none block w-full px-3 py-3 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Full Name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
        />
      </div>

      <div>
        <label htmlFor="roleType" className="block text-sm font-medium text-gray-700 mb-1">I am a</label>
        <select
          id="roleType"
          name="roleType"
          required
          className="appearance-none block w-full px-3 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white"
          value={roleType}
          onChange={(e) => setRoleType(e.target.value)}
        >
          <option value="user">Gym User</option>
          <option value="admin">Gym Admin</option>
        </select>
      </div>

      <div>
        <label htmlFor="signup-email" className="sr-only">Email address</label>
        <input
          id="signup-email"
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
        <label htmlFor="signup-password" className="sr-only">Password</label>
        <input
          id="signup-password"
          name="password"
          type="password"
          autoComplete="new-password"
          required
          className="appearance-none block w-full px-3 py-3 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          placeholder="Password (min. 8 characters)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <div>
        <button
          type="submit"
          className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-600"
        >
          Sign Up
        </button>
      </div>
      {error && (
        <p className="mt-2 text-center text-sm text-red-600 p-3 bg-red-100 rounded-md">
          {error}
        </p>
      )}
      {successMessage && (
        <p className="mt-2 text-center text-sm text-green-600 p-3 bg-green-100 rounded-md">
          {successMessage}
        </p>
      )}
    </form>
  );
};

export default SignUpForm;
