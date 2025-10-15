import React, { useState } from 'react';

const Quiz = ({ question, answer, onAnswer }) => {
  const [score, setScore] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [isAnimating, setIsAnimating] = useState(false);

  const handleSubmit = (userAnswer) => {
    if (score !== null) return; // Prevent multiple submissions
    
    setIsAnimating(true);
    setSelectedAnswer(userAnswer);
    
    setTimeout(() => {
      const isCorrect = userAnswer === answer;
      setScore(isCorrect ? 1 : 0);
      setIsAnimating(false);
      
      if (onAnswer) {
        onAnswer(isCorrect);
      }
    }, 500);
  };

  const getButtonClass = (option) => {
    if (score === null) return 'btn btn-secondary';
    
    if (selectedAnswer === option) {
      return answer === option ? 'btn btn-success' : 'btn btn-danger';
    }
    
    if (answer === option) {
      return 'btn btn-outline';
    }
    
    return 'btn btn-secondary opacity-50';
  };

  return (
    <div className="quiz hover-lift">
      <div className="quiz-question">{question}</div>
      
      <div className="quiz-options">
        <button 
          onClick={() => handleSubmit('Yes')} 
          className={`${getButtonClass('Yes')} ${isAnimating ? 'pulse' : ''}`}
          disabled={score !== null}
        >
          ✅ Yes
        </button>
        <button 
          onClick={() => handleSubmit('No')} 
          className={`${getButtonClass('No')} ${isAnimating ? 'pulse' : ''}`}
          disabled={score !== null}
        >
          ❌ No
        </button>
      </div>
      
      {score !== null && (
        <div className="quiz-score animate-slideIn">
          {score === 1 ? (
            <div className="text-center">
              <div className="text-success text-lg mb-2">🎉 Correct! Well done!</div>
              <div className="text-sm text-secondary">Great job on identifying the phishing indicator!</div>
            </div>
          ) : (
            <div className="text-center">
              <div className="text-danger text-lg mb-2">❌ Incorrect</div>
              <div className="text-sm text-secondary">The correct answer is: <strong>{answer}</strong></div>
              <div className="text-sm text-secondary mt-2">Keep learning to improve your phishing detection skills!</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Quiz;