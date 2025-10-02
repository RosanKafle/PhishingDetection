import React, { useState } from 'react';

const Quiz = ({ question, answer }) => {
  const [score, setScore] = useState(null);

  const handleSubmit = (userAnswer) => {
    setScore(userAnswer === answer ? 1 : 0);
  };

  return (
    <div className="quiz">
      <p>{question}</p>
      <button onClick={() => handleSubmit('Yes')}>Yes</button>
      <button onClick={() => handleSubmit('No')}>No</button>
      {score !== null && <p>Score: {score}/1</p>}
    </div>
  );
};

export default Quiz;