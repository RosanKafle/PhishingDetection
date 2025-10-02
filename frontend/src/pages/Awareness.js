import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Awareness = () => {
  const [articles, setArticles] = useState([]);
  const [quizzes, setQuizzes] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const res = await axios.get('http://localhost:5000/api/content');
        const all = res.data || [];
        setArticles(all.filter(c => c.type === 'article'));
        setQuizzes(all.filter(c => c.type === 'quiz'));
      } catch (err) {
        setError('Failed to load awareness content');
      }
    };
    fetchContent();
  }, []);

  return (
    <div>
      <h2>Security Awareness</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <section>
        <h3>Articles</h3>
        {articles.length === 0 && <p>No articles yet.</p>}
        {articles.map(a => (
          <div key={a._id} className="card">
            <h4>{a.title}</h4>
            <p>{String(a.content)}</p>
          </div>
        ))}
      </section>

      <section>
        <h3>Quizzes</h3>
        {quizzes.length === 0 && <p>No quizzes yet.</p>}
        {quizzes.map(q => (
          <div key={q._id} className="card">
            <h4>{q.title}</h4>
            <pre>{typeof q.content === 'object' ? JSON.stringify(q.content, null, 2) : String(q.content)}</pre>
          </div>
        ))}
      </section>
    </div>
  );
};

export default Awareness;


