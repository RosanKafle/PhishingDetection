import React from 'react';
import { Navigate } from 'react-router-dom';
import { getAuthToken } from '../utils/auth';

const ProtectedRoute = ({ children }) => {
  const token = getAuthToken();
  return token ? children : <Navigate to="/" replace />;
};

export default ProtectedRoute;