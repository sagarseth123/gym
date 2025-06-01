import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('authToken');
  const location = useLocation(); // Optional: to redirect back after login

  if (!token) {
    // User not authenticated
    // You can pass the current location to redirect back after login
    // e.g., return <Navigate to="/login" state={{ from: location }} replace />;
    return <Navigate to="/login" replace />;
  }

  return children; // Render the protected component
};

export default ProtectedRoute;
