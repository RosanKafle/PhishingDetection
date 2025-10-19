import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { getAuthToken, removeAuthToken, isAdmin } from '../utils/auth';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const isLoggedIn = !!getAuthToken();

  const handleLogout = () => {
    removeAuthToken();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <Link to="/dashboard" className="navbar-brand">
        Phishing Detector
      </Link>
      
      <ul className="navbar-nav">
        {isLoggedIn ? (
          <>
            <li>
              <Link 
                to="/dashboard" 
                className={location.pathname === '/dashboard' ? 'active' : ''}
              >
                🏠 Dashboard
              </Link>
            </li>
            <li>
              <Link 
                to="/awareness" 
                className={location.pathname === '/awareness' ? 'active' : ''}
              >
                📚 Awareness
              </Link>
            </li>
            {isAdmin() && (
              <li>
                <Link 
                  to="/admin" 
                  className={location.pathname === '/admin' ? 'active' : ''}
                >
                  ⚙️ Admin
                </Link>
              </li>
            )}
            <li>
              <button onClick={handleLogout} className="btn btn-secondary">
                🚪 Logout
              </button>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link 
                to="/" 
                className={location.pathname === '/' ? 'active' : ''}
              >
                🔐 Login
              </Link>
            </li>
            <li>
              <Link 
                to="/register" 
                className={location.pathname === '/register' ? 'active' : ''}
              >
                📝 Register
              </Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;