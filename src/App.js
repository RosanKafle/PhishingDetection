import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Awareness from './pages/Awareness';
import AdminPanel from './pages/AdminPanel';
import './styles.css';

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route 
            path="/dashboard" 
            element={<ProtectedRoute><Dashboard /></ProtectedRoute>} 
          />
          <Route 
            path="/awareness" 
            element={<ProtectedRoute><Awareness /></ProtectedRoute>} 
          />
          <Route 
            path="/admin" 
            element={<ProtectedRoute><AdminPanel /></ProtectedRoute>} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;