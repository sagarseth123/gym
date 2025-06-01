import React from 'react';
import { Navigate } from 'react-router-dom'; // Removed useLocation

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('authToken');
  // const location = useLocation(); // Optional: to redirect back after login - REMOVED

  if (!token) {
    // User not authenticated
    // You can pass the current location to redirect back after login
    // e.g., return <Navigate to="/login" state={{ from: location }} replace />;
    // For that, useLocation would be needed. For now, it's not used.
    return <Navigate to="/login" replace />;
  }

  return children; // Render the protected component
};

export default ProtectedRoute;
