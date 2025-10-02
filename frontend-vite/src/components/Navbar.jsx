import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getAuthToken, removeAuthToken } from '../utils/auth';

const Navbar = () => {
  const navigate = useNavigate();
  const isLoggedIn = !!getAuthToken();

  const handleLogout = () => {
    removeAuthToken();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <Link to="/dashboard">Phishing Detector</Link>
      <Link to="/python-scripts">Python Scripts</Link>
      {isLoggedIn ? (
        <>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/awareness">Awareness</Link>
          <Link to="/admin">Admin</Link>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <>
          <Link to="/">Login</Link>
          <Link to="/register">Register</Link>
        </>
      )}
    </nav>
  );
};

export default Navbar;