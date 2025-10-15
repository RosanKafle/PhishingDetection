import React, { useState } from 'react';
import axios from 'axios';
import { getAuthToken } from '../utils/auth';

const AdminPanel = () => {
  const [type, setType] = useState('article');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await axios.post('http://localhost:5000/api/content/add', { type, title, content }, {
        headers: { Authorization: `Bearer ${getAuthToken()}` }
      });
      alert('Content added successfully!');
      setTitle('');
      setContent('');
    } catch (err) {
      alert('Error adding content: ' + (err.response?.data?.error || 'Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      {/* Header */}
      <div className="card mb-5 hover-lift">
        <div className="text-center">
          <h1 className="card-title gradient-text">⚙️ Admin Panel</h1>
          <p className="card-subtitle">Manage awareness content and educational materials</p>
          <div className="mt-4">
            <div className="badge badge-primary">Content Management</div>
            <div className="badge badge-success">Analytics Dashboard</div>
            <div className="badge badge-info">User Insights</div>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-4 mb-5">
        <div className="card hover-lift">
          <div className="text-center">
            <div className="text-4xl mb-2">👥</div>
            <div className="text-3xl font-bold text-primary">0</div>
            <div className="text-secondary">Total Users</div>
          </div>
        </div>
        
        <div className="card hover-lift">
          <div className="text-center">
            <div className="text-4xl mb-2">🔍</div>
            <div className="text-3xl font-bold text-info">0</div>
            <div className="text-secondary">Detections</div>
          </div>
        </div>
        
        <div className="card hover-lift">
          <div className="text-center">
            <div className="text-4xl mb-2">📚</div>
            <div className="text-3xl font-bold text-success">0</div>
            <div className="text-secondary">Articles</div>
          </div>
        </div>
        
        <div className="card hover-lift">
          <div className="text-center">
            <div className="text-4xl mb-2">🧠</div>
            <div className="text-3xl font-bold text-warning">0</div>
            <div className="text-secondary">Quizzes</div>
          </div>
        </div>
      </div>

      {/* Content Creation */}
      <div className="card mb-5 hover-lift">
        <div className="card-header">
          <h2 className="card-title">📝 Create New Content</h2>
          <p className="card-subtitle">Add educational articles and interactive quizzes</p>
        </div>
        
        <form onSubmit={handleSubmit} className="form">
          <div className="grid grid-cols-2 gap-4">
            <div className="form-group">
              <label htmlFor="type" className="form-label">
                <span className="flex items-center gap-2">
                  📋 Content Type
                </span>
              </label>
              <select 
                id="type"
                value={type} 
                onChange={(e) => setType(e.target.value)}
                className="form-select"
              >
                <option value="article">📖 Educational Article</option>
                <option value="quiz">🧠 Interactive Quiz</option>
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="title" className="form-label">
                <span className="flex items-center gap-2">
                  📝 Title
                </span>
              </label>
              <input 
                id="title"
                type="text" 
                value={title} 
                onChange={(e) => setTitle(e.target.value)} 
                className="form-input"
                placeholder="Enter content title" 
                required 
              />
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="content" className="form-label">
              <span className="flex items-center gap-2">
                📄 Content {type === 'quiz' ? '(JSON format for quiz questions)' : ''}
              </span>
            </label>
            <textarea 
              id="content"
              value={content} 
              onChange={(e) => setContent(e.target.value)} 
              className="form-textarea"
              placeholder={
                type === 'quiz' 
                  ? '{"questions": [{"question": "Your question?", "answer": "Yes"}]}'
                  : "Enter the article content here..."
              }
              rows="10"
              required 
            />
            <div className="mt-2 text-sm text-secondary">
              Character count: {content.length} / 10000
            </div>
          </div>
          
          <div className="flex gap-3">
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? (
                <span className="loading">
                  <span className="spinner"></span>
                  Adding content...
                </span>
              ) : (
                <>
                  ➕ Add Content
                </>
              )}
            </button>
            
            <button 
              type="button" 
              className="btn btn-secondary"
              onClick={() => {
                setTitle('');
                setContent('');
              }}
            >
              🗑️ Clear Form
            </button>
          </div>
        </form>
        
        {type === 'quiz' && (
          <div className="mt-6 p-4" style={{ background: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)' }}>
            <h4 className="mb-3">📝 Quiz JSON Format Example:</h4>
            <pre style={{ 
              background: 'var(--bg-primary)', 
              padding: '1rem', 
              borderRadius: 'var(--radius-sm)',
              overflow: 'auto',
              fontSize: '0.9rem',
              border: '1px solid var(--border-color)'
            }}>
{`{
  "questions": [
    {
      "question": "Is it safe to click links in suspicious emails?",
      "answer": "No"
    },
    {
      "question": "Should you verify sender identity when in doubt?",
      "answer": "Yes"
    }
  ]
}`}
            </pre>
          </div>
        )}
      </div>
      
      {/* Content Management */}
      <div className="card mb-5">
        <div className="card-header">
          <h2 className="card-title">📊 Content Management</h2>
          <p className="card-subtitle">View and manage existing content</p>
        </div>
        
        <div className="grid grid-cols-3 gap-4 mb-4">
          <button className="btn btn-secondary hover-lift">
            <span className="flex items-center justify-center gap-2">
              📋 View All Content
            </span>
          </button>
          <button className="btn btn-secondary hover-lift">
            <span className="flex items-center justify-center gap-2">
              ✏️ Edit Content
            </span>
          </button>
          <button className="btn btn-danger hover-lift">
            <span className="flex items-center justify-center gap-2">
              🗑️ Delete Content
            </span>
          </button>
        </div>
        
        <div className="alert alert-info">
          <strong>ℹ️ Note:</strong> Content management features will be fully available once the backend is connected. Currently, you can create new content using the form above.
        </div>
      </div>
      
      {/* Analytics Dashboard */}
      <div className="card mb-5">
        <div className="card-header">
          <h2 className="card-title">📈 Analytics Dashboard</h2>
          <p className="card-subtitle">Platform usage and performance metrics</p>
        </div>
        
        <div className="grid grid-cols-2 gap-6">
          <div className="content">
            <h3 className="mb-4">📊 User Engagement</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span>Daily Active Users</span>
                <span className="font-bold text-primary">0</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Content Views</span>
                <span className="font-bold text-info">0</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Quiz Completions</span>
                <span className="font-bold text-success">0</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Detection Requests</span>
                <span className="font-bold text-warning">0</span>
              </div>
            </div>
          </div>
          
          <div className="content">
            <h3 className="mb-4">🎯 Performance Metrics</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span>Average Detection Time</span>
                <span className="font-bold text-primary">0.5s</span>
              </div>
              <div className="flex justify-between items-center">
                <span>System Uptime</span>
                <span className="font-bold text-success">99.9%</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Content Accuracy</span>
                <span className="font-bold text-info">95%</span>
              </div>
              <div className="flex justify-between items-center">
                <span>User Satisfaction</span>
                <span className="font-bold text-warning">4.8/5</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* System Status */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">🔧 System Status</h2>
          <p className="card-subtitle">Monitor platform health and performance</p>
        </div>
        
        <div className="grid grid-cols-4">
          <div className="content text-center hover-lift">
            <div className="text-4xl mb-3">🟢</div>
            <h3>Backend API</h3>
            <div className="badge badge-success">Online</div>
            <p className="text-secondary mt-2">All systems operational</p>
          </div>
          
          <div className="content text-center hover-lift">
            <div className="text-4xl mb-3">🟢</div>
            <h3>Database</h3>
            <div className="badge badge-success">Connected</div>
            <p className="text-secondary mt-2">Data sync active</p>
          </div>
          
          <div className="content text-center hover-lift">
            <div className="text-4xl mb-3">🟢</div>
            <h3>Detection Engine</h3>
            <div className="badge badge-success">Running</div>
            <p className="text-secondary mt-2">AI models loaded</p>
          </div>
          
          <div className="content text-center hover-lift">
            <div className="text-4xl mb-3">🟡</div>
            <h3>Content CDN</h3>
            <div className="badge badge-warning">Limited</div>
            <p className="text-secondary mt-2">Some features offline</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;