import React, { useState, useEffect, useMemo, useCallback } from 'react';
import axios from 'axios';
import { getAuthToken } from '../utils/auth';
import Quiz from '../components/Quiz';

const Awareness = () => {
  const [content, setContent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [quizScore, setQuizScore] = useState(0);

  const fetchContent = useCallback(async () => {
    try {
      const response = await axios.get('http://localhost:5001/api/content', {
        headers: { Authorization: `Bearer ${getAuthToken()}` },
        timeout: 10000
      });
      setContent(response.data);
    } catch (error) {
      // Fallback content if backend is not available
      setContent([
        {
          id: 1,
          type: 'article',
          title: 'What is Phishing?',
          content: 'Phishing is a cyber attack that uses disguised email as a weapon. The goal is to trick the email recipient into believing that the message is something they want or need — a request from their bank, for instance, or a note from someone in their company — and to click a link or download an attachment.'
        },
        {
          id: 2,
          type: 'article',
          title: 'Common Phishing Techniques',
          content: '1. Email Spoofing: Attackers forge email headers to make messages appear to come from legitimate sources.\n2. Link Manipulation: Malicious links that appear to lead to legitimate websites.\n3. Website Forgery: Fake websites that mimic legitimate ones.\n4. Social Engineering: Manipulating people into performing actions or divulging confidential information.'
        },
        {
          id: 3,
          type: 'quiz',
          title: 'Phishing Awareness Quiz',
          content: {
            questions: [
              { question: 'Is it safe to click on links in emails from unknown senders?', answer: 'No' },
              { question: 'Should you verify suspicious emails by calling the sender?', answer: 'Yes' },
              { question: 'Is it okay to share your password with IT support via email?', answer: 'No' },
              { question: 'Should you trust emails asking for urgent financial information?', answer: 'No' },
              { question: 'Is it safe to download attachments from unknown sources?', answer: 'No' },
              { question: 'Should you check the sender\'s email address carefully?', answer: 'Yes' },
              { question: 'Is it okay to enter personal information on suspicious websites?', answer: 'No' },
              { question: 'Should you report suspected phishing emails to IT?', answer: 'Yes' },
              { question: 'Is it safe to use public Wi-Fi for banking?', answer: 'No' },
              { question: 'Should you use two-factor authentication when available?', answer: 'Yes' }
            ]
          }
        }
      ]);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchContent();
  }, [fetchContent]);

  const handleQuizAnswer = useCallback((questionIndex, isCorrect) => {
    if (isCorrect) {
      setQuizScore(prev => prev + 1);
    }
  }, []);

  const articleCount = useMemo(() => 
    content.filter(c => c.type === 'article').length, [content]
  );
  
  const quizCount = useMemo(() => 
    content.filter(c => c.type === 'quiz').length, [content]
  );
  
  const masteryLevel = useMemo(() => 
    quizCount > 0 ? Math.round((quizScore / (quizCount * 3)) * 100) : 0, 
    [quizScore, quizCount]
  );

  if (loading) {
    return (
      <div className="container">
        <div className="card text-center">
          <div className="loading">
            <span className="spinner"></span>
            Loading awareness content...
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      {/* Header */}
      <div className="card mb-5 hover-lift">
        <div className="text-center">
          <h1 className="card-title gradient-text">📚 Phishing Awareness Center</h1>
          <p className="card-subtitle">
            Learn about phishing attacks, how to identify them, and protect yourself online
          </p>
          <div className="mt-4">
            <div className="badge badge-primary">Interactive Learning</div>
            <div className="badge badge-success">Expert Knowledge</div>
            <div className="badge badge-info">Real-world Examples</div>
          </div>
        </div>
      </div>

      {/* Progress Tracker */}
      <div className="card mb-5">
        <div className="card-header">
          <h2 className="card-title">📈 Learning Progress</h2>
          <p className="card-subtitle">Track your cybersecurity knowledge journey</p>
        </div>
        
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-3xl mb-2">📖</div>
            <div className="text-2xl font-bold text-primary">{articleCount}</div>
            <div className="text-secondary">Articles Read</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl mb-2">🧠</div>
            <div className="text-2xl font-bold text-warning">{quizScore}</div>
            <div className="text-secondary">Quiz Points</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl mb-2">🎯</div>
            <div className="text-2xl font-bold text-success">
              {masteryLevel}%
            </div>
            <div className="text-secondary">Mastery Level</div>
          </div>
        </div>
      </div>

      {/* Educational Content */}
      {content.map((item, index) => (
        <div key={item.id} className="card hover-lift">
          <div className="card-header">
            <div className="flex items-center justify-between">
              <h2 className="card-title">
                {item.type === 'article' ? '📖' : '🧠'} {item.title}
              </h2>
              <div className="badge badge-info">
                {item.type === 'article' ? 'Article' : 'Quiz'}
              </div>
            </div>
          </div>
          
          {item.type === 'article' ? (
            <div className="content">
              <div className="prose">
                <p style={{ whiteSpace: 'pre-line', lineHeight: '1.8', fontSize: '1.1rem' }}>
                  {item.content}
                </p>
              </div>
              
              {/* Article Actions */}
              <div className="mt-4 flex gap-3">
                <button className="btn btn-secondary btn-sm">
                  📌 Bookmark
                </button>
                <button className="btn btn-secondary btn-sm">
                  📤 Share
                </button>
                <button className="btn btn-secondary btn-sm">
                  💬 Discuss
                </button>
              </div>
            </div>
          ) : item.type === 'quiz' ? (
            <div>
              <div className="alert alert-info mb-4">
                <strong>🧠 Knowledge Check:</strong> Test your understanding with this interactive quiz
              </div>
              
              {item.content.questions && item.content.questions
                .slice(0, 5)
                .map((q, qIndex) => (
                <div key={qIndex} className="mb-6">
                  <Quiz 
                    question={q.question}
                    answer={q.answer}
                    onAnswer={(isCorrect) => handleQuizAnswer(qIndex, isCorrect)}
                  />
                </div>
              ))}
              
              {quizScore > 0 && (
                <div className="quiz-score text-center mt-6 p-4" style={{ background: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)' }}>
                  <div className="text-2xl font-bold mb-2">
                    Your Score: {quizScore}/5
                  </div>
                  <div className="progress mb-3">
                    <div 
                      className="progress-bar" 
                      style={{ width: `${(quizScore / 5) * 100}%` }}
                    ></div>
                  </div>
                  <div className="mt-2">
                    {quizScore === 5 ? (
                      <span className="text-success text-lg">🎉 Perfect! You're a phishing detection expert!</span>
                    ) : quizScore >= 4 ? (
                      <span className="text-warning text-lg">👍 Good job! Keep learning!</span>
                    ) : (
                      <span className="text-danger text-lg">📚 Keep studying to improve your knowledge!</span>
                    )}
                  </div>
                </div>
              )}
            </div>
          ) : null}
        </div>
      ))}

      {/* Best Practices */}
      <div className="card mb-5">
        <div className="card-header">
          <h2 className="card-title">✅ Security Best Practices</h2>
          <p className="card-subtitle">Follow these guidelines to stay safe online</p>
        </div>
        
        <div className="grid grid-cols-3">
          <div className="content hover-lift">
            <div className="text-center mb-4">
              <div className="text-4xl">🔐</div>
              <h3>Authentication</h3>
            </div>
            <ul>
              <li>Use strong, unique passwords</li>
              <li>Enable two-factor authentication</li>
              <li>Use password managers</li>
              <li>Never share login credentials</li>
            </ul>
          </div>
          
          <div className="content hover-lift">
            <div className="text-center mb-4">
              <div className="text-4xl">📧</div>
              <h3>Email Safety</h3>
            </div>
            <ul>
              <li>Verify sender email addresses</li>
              <li>Look for spelling and grammar mistakes</li>
              <li>Be suspicious of urgent requests</li>
              <li>Never click suspicious links</li>
            </ul>
          </div>
          
          <div className="content hover-lift">
            <div className="text-center mb-4">
              <div className="text-4xl">🌐</div>
              <h3>Web Browsing</h3>
            </div>
            <ul>
              <li>Check URLs before clicking</li>
              <li>Look for HTTPS in URLs</li>
              <li>Use reputable websites</li>
              <li>Keep browsers updated</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Red Flags Section */}
      <div className="card mb-5">
        <div className="card-header">
          <h2 className="card-title">🚨 Warning Signs to Watch For</h2>
          <p className="card-subtitle">Common indicators of phishing attempts</p>
        </div>
        
        <div className="grid grid-cols-3">
          <div className="content hover-lift">
            <div className="text-center mb-4">
              <div className="text-4xl">📧</div>
              <h3>Email Red Flags</h3>
            </div>
            <ul>
              <li>Generic greetings like "Dear Customer"</li>
              <li>Requests for immediate action</li>
              <li>Threats of account closure</li>
              <li>Suspicious sender email addresses</li>
              <li>Poor grammar and spelling</li>
              <li>Requests for sensitive information</li>
              <li>Unexpected attachments</li>
            </ul>
          </div>
          
          <div className="content hover-lift">
            <div className="text-center mb-4">
              <div className="text-4xl">🔗</div>
              <h3>URL Red Flags</h3>
            </div>
            <ul>
              <li>Misspelled domain names</li>
              <li>Suspicious subdomains</li>
              <li>HTTP instead of HTTPS</li>
              <li>IP addresses instead of domains</li>
              <li>Shortened URLs from unknown sources</li>
              <li>Unusual characters in URLs</li>
            </ul>
          </div>
          
          <div className="content hover-lift">
            <div className="text-center mb-4">
              <div className="text-4xl">🎭</div>
              <h3>Social Engineering Tactics</h3>
            </div>
            <ul>
              <li>Creating urgency or fear</li>
              <li>Pretending to be authority figures</li>
              <li>Offering too-good-to-be-true deals</li>
              <li>Requesting personal information</li>
              <li>Using emotional manipulation</li>
              <li>Creating fake emergencies</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Resources */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">📚 Additional Resources</h2>
          <p className="card-subtitle">Learn more about cybersecurity and phishing protection</p>
        </div>
        
        <div className="grid grid-cols-4">
          <div className="content text-center hover-lift">
            <div className="text-4xl mb-3">🎓</div>
            <h3>Training</h3>
            <p className="text-secondary mb-4">Take cybersecurity awareness courses</p>
            <button className="btn btn-primary">Start Learning</button>
          </div>
          
          <div className="content text-center hover-lift">
            <div className="text-4xl mb-3">📊</div>
            <h3>Reports</h3>
            <p className="text-secondary mb-4">View latest phishing statistics</p>
            <div className="mt-4">
              <div className="mb-3">
                <a href="https://www.ic3.gov/Media/PDF/AnnualReport/2023_IC3Report.pdf" target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-outline-primary mb-2 d-block">
                  FBI IC3 2023 Report
                </a>
                <a href="https://www.verizon.com/business/resources/reports/dbir/" target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-outline-primary mb-2 d-block">
                  Verizon DBIR 2024
                </a>
                <a href="https://www.proofpoint.com/us/threat-insight/post/state-phish-2024" target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-outline-primary mb-2 d-block">
                  Proofpoint State of Phish
                </a>
                <a href="https://www.cisa.gov/news-events/cybersecurity-advisories" target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-outline-primary d-block">
                  CISA Advisories
                </a>
              </div>
            </div>
          </div>
          
          <div className="content text-center hover-lift">
            <div className="text-4xl mb-3">🛠️</div>
            <h3>Tools</h3>
            <p className="text-secondary mb-4">Access security tools and utilities</p>
            <button className="btn btn-secondary">Browse Tools</button>
          </div>
          
          <div className="content text-center hover-lift">
            <div className="text-4xl mb-3">📞</div>
            <h3>Support</h3>
            <p className="text-secondary mb-4">Get help and report incidents</p>
            <button className="btn btn-secondary">Contact Support</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Awareness;