import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Awareness from './pages/Awareness';
import AdminPanel from './pages/AdminPanel';
import PythonScriptLauncher from './components/PythonScriptLauncher';
import './styles.css';

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/awareness" element={<Awareness />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/python-scripts" element={<PythonScriptLauncher />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;