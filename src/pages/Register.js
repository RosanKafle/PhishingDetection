import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { setAuthToken } from '../utils/auth';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await axios.post('http://localhost:5000/api/auth/register', { username, email, password });
      const res = await axios.post('http://localhost:5000/api/auth/login', { email, password });
      setAuthToken(res.data.token);
      navigate('/dashboard');
    } catch (err) {
      alert(err.response?.data?.error || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="form-container">
        <div className="card hover-lift">
          <div className="card-header">
            <div className="text-center">
              <div className="text-6xl mb-4">🚀</div>
              <h1 className="card-title gradient-text">Create Account</h1>
              <p className="card-subtitle">Join Phishing Detector to protect yourself online</p>
            </div>
          </div>
          
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group">
              <label htmlFor="username" className="form-label">
                <span className="flex items-center gap-2">
                  👤 Username
                </span>
              </label>
              <input 
                id="username"
                type="text" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} 
                className="form-input"
                placeholder="Choose a unique username" 
                required 
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="email" className="form-label">
                <span className="flex items-center gap-2">
                  📧 Email Address
                </span>
              </label>
              <input 
                id="email"
                type="email" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
                className="form-input"
                placeholder="Enter your email address" 
                required 
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="password" className="form-label">
                <span className="flex items-center gap-2">
                  🔒 Password
                </span>
              </label>
              <input 
                id="password"
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                className="form-input"
                placeholder="Create a strong password" 
                required 
              />
              <div className="mt-2 text-sm text-secondary">
                Password strength: {password.length >= 8 ? 'Strong' : password.length >= 6 ? 'Medium' : 'Weak'}
              </div>
            </div>
            
            <button 
              type="submit" 
              className="btn btn-primary w-full"
              disabled={loading}
            >
              {loading ? (
                <span className="loading">
                  <span className="spinner"></span>
                  Creating account...
                </span>
              ) : (
                <>
                  🎉 Create Account
                </>
              )}
            </button>
          </form>
          
          <div className="text-center mt-4">
            <div className="divider">
              <span className="text-secondary">or</span>
            </div>
            <p className="text-secondary mt-4">
              Already have an account? 
              <Link to="/" className="text-primary font-semibold" style={{ marginLeft: '0.5rem' }}>
                Sign in here
              </Link>
            </p>
          </div>
          
          {/* Benefits */}
          <div className="mt-6 p-4" style={{ background: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)' }}>
            <h4 className="text-center mb-3">🎯 What You Get</h4>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="flex items-center gap-2">
                <span className="text-success">✅</span>
                <span>Real-time Detection</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-success">✅</span>
                <span>Educational Content</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-success">✅</span>
                <span>Interactive Quizzes</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-success">✅</span>
                <span>Detection History</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;