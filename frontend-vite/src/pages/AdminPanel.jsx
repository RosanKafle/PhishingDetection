import React, { useState } from 'react';
import axios from 'axios';
import { getAuthToken } from '../utils/auth';

const AdminPanel = () => {
  const [type, setType] = useState('article');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/content/add', { type, title, content }, {
        headers: { Authorization: `Bearer ${getAuthToken()}` }
      });
      alert('Content added');
      setTitle('');
      setContent('');
    } catch (err) {
      alert('Error adding content');
    }
  };

  return (
    <div>
      <h2>Admin Panel - Add Awareness Content</h2>
      <form onSubmit={handleSubmit} className="form">
        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="article">Article</option>
          <option value="quiz">Quiz</option>
        </select>
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Title" required />
        <textarea value={content} onChange={(e) => setContent(e.target.value)} placeholder="Content (JSON for quizzes)" required />
        <button type="submit">Add</button>
      </form>
    </div>
  );
};

export default AdminPanel;