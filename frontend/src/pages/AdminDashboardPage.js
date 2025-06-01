import React from 'react';
import { useNavigate } from 'react-router-dom';

// Assuming App.css or another global CSS file has basic button styling
// import './AdminDashboardPage.css'; // If specific styles are needed

const AdminDashboardPage = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    // Optionally, remove other related items if any (e.g., tokenType, user details)
    // localStorage.removeItem('tokenType');
    navigate('/login');
  };

  return (
    <div className="dashboard-container"> {/* Optional class for styling */}
      <h2>Admin Dashboard</h2>
      <p>Welcome to your dashboard! More features coming soon.</p>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default AdminDashboardPage;
