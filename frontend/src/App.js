import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import './App.css';

// Import the actual page components
import AdminSignupPage from './pages/AdminSignupPage';
import AdminLoginPage from './pages/AdminLoginPage';
import AdminDashboardPage from './pages/AdminDashboardPage'; // Import AdminDashboardPage

// Import ProtectedRoute component
import ProtectedRoute from './components/ProtectedRoute';

// Placeholder components (will be moved to separate files later)
const HomePage = () => <div><h2>Home Page</h2><p>Welcome to the Gym Platform!</p></div>;
// const AdminLoginPage = () => <div><h2>Admin Login Page (Placeholder)</h2></div>; // Already removed
// const AdminSignupPage = () => <div><h2>Admin Signup Page (Placeholder)</h2></div>; // Already removed
// const AdminDashboardPage = () => <div><h2>Admin Dashboard (Placeholder)</h2></div>; // Remove placeholder

function App() {
  return (
    <div className="App">
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/login">Admin Login</Link></li>
          <li><Link to="/signup">Admin Signup</Link></li>
          <li><Link to="/admin/dashboard">Admin Dashboard (Test)</Link></li>
        </ul>
      </nav>

      <hr />

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<AdminLoginPage />} />
        <Route path="/signup" element={<AdminSignupPage />} />
        <Route
          path="/admin/dashboard"
          element={
            <ProtectedRoute>
              <AdminDashboardPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </div>
  );
}

export default App;
