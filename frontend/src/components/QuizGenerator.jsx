import React, { useState } from 'react';
import { generateQuiz } from '../services/api';

const QuizGenerator = () => {
  const [inputText, setInputText] = useState('');
  const [topic, setTopic] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quizData, setQuizData] = useState(null);
  const [selectedAnswers, setSelectedAnswers] = useState({});

  const handleGenerate = async () => {
    setError(null);
    setQuizData(null);
    setSelectedAnswers({});

    if (!inputText || !topic) {
      setError({
        title: "Missing Information",
        message: "Please upload text and define a topic first."
      });
      return;
    }

    setIsLoading(true);

    try {
      const data = await generateQuiz(inputText, topic, "medium");
      setQuizData(data);
    } catch (err) {
      if (err.message === "SERVICE_AT_CAPACITY") {
        setError({
          title: "Service at Capacity 🚦",
          message: "We are using the free AI tier which limits requests. Please wait 1-2 minutes and try again."
        });
      } else {
        setError({
          title: "Generation Failed",
          message: "The AI could not process this text. Try a shorter section."
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleOptionClick = (questionId, selectedOptionIndex) => {
    if (selectedAnswers[questionId] !== undefined) return;

    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: selectedOptionIndex
    }));
  };

  return (
    <div>
      <div className="input-card">
        <div className="input-group">
          <textarea
            className="styled-textarea"
            rows="5"
            placeholder="Paste your study notes or textbook content here..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
        </div>
        <div className="input-group">
          <input
            type="text"
            className="styled-input"
            placeholder="Subject / Topic (e.g., 'French Revolution')"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
        </div>
        
        <button
          onClick={handleGenerate}
          disabled={isLoading}
          className="generate-btn"
        >
          {isLoading ? (
            <>
              <div className="spinner"></div>
              Generating Quiz...
            </>
          ) : (
            "✨ Generate Study Quiz"
          )}
        </button>
      </div>

      {error && (
        <div className="error-box">
          <h3 className="error-title">{error.title}</h3>
          <p className="error-msg">{error.message}</p>
        </div>
      )}

      {quizData && quizData.questions && (
        <div className="quiz-container">
          <h2 className="topic-title">
            Topic: {quizData.topic}
          </h2>

          {quizData.questions.map((q, index) => {
            const selectedOptionIndex = selectedAnswers[q.id];
            const isAnswered = selectedOptionIndex !== undefined;

            let correctOptionIndex = -1;
            q.options.forEach((option, idx) => {
              const optionLetter = String.fromCharCode(65 + idx);
              const fullOption = `${optionLetter}. ${option}`;
              if (fullOption === q.answer || option === q.answer || fullOption.trim() === q.answer.trim()) {
                correctOptionIndex = idx;
              }
            });

            const isCorrect = isAnswered && selectedOptionIndex === correctOptionIndex;

            return (
              <div key={q.id || index} className="question-card">
                <div className="question-header">
                  <span className="q-badge">Q{index + 1}</span>
                  <h3 className="q-text">{q.question}</h3>
                </div>

                <div className="options-grid">
                  {q.options.map((option, idx) => {
                    const optionLetter = String.fromCharCode(65 + idx);
                    const isThisCorrect = idx === correctOptionIndex;
                    const isThisSelected = idx === selectedOptionIndex;

                    let optionClass = "option-item";
                    if (isAnswered) {
                      if (isThisCorrect) {
                        optionClass += " option-correct";
                      } else if (isThisSelected) {
                        optionClass += " option-incorrect";
                      } else {
                        optionClass += " option-disabled";
                      }
                    } else {
                      optionClass += " option-clickable";
                    }

                    return (
                      <div
                        key={idx}
                        className={optionClass}
                        onClick={() => !isAnswered && handleOptionClick(q.id, idx)}
                      >
                        <span className="opt-letter">{optionLetter}.</span>
                        {option}
                      </div>
                    );
                  })}
                </div>

                {isAnswered && (
                  <div className="answer-box">
                    <p className="answer-correct">
                      {isCorrect ? "✅ Correct!" : `❌ Incorrect. Correct answer: ${q.answer}`}
                    </p>
                    <p className="answer-explanation">{q.explanation}</p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default QuizGenerator;