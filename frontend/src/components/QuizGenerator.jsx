import React, { useState } from 'react';
import { generateQuiz } from '../services/api';

const QuizGenerator = () => {
  const [inputText, setInputText] = useState('');
  const [topic, setTopic] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quizData, setQuizData] = useState(null);
  // Track selected answer index for each question ID
  const [selectedAnswers, setSelectedAnswers] = useState({});

  const handleGenerate = async () => {
    // 1. Reset State
    setError(null);
    setQuizData(null);
    setSelectedAnswers({});

    // 2. Validate Input
    if (!inputText.trim() || !topic.trim()) {
      setError({
        title: "Missing Information",
        message: "Please upload text and define a topic first."
      });
      return;
    }

    // 3. Set Loading (Requirement: Spinner)
    setIsLoading(true);

    try {
      // 4. API Call
      const data = await generateQuiz(inputText, topic, "medium");
      
      // 5. Data Keys Check (Requirement: data.topic, data.questions)
      if (!data || !data.questions) {
        throw new Error("Invalid format received from AI");
      }
      
      setQuizData(data);
    } catch (err) {
      // 6. Error Handling (Requirement: 429 Service Capacity)
      if (err.message === "SERVICE_AT_CAPACITY") {
        setError({
          title: "Service at Capacity 🚦",
          message: "We are using the free AI tier (20 req/day). Please wait a moment or try again tomorrow."
        });
      } else {
        setError({
          title: "Generation Failed",
          message: err.message || "The AI could not process this text. Try a shorter section."
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleOptionClick = (questionId, selectedOptionIndex) => {
    // Prevent changing answer if already selected
    if (selectedAnswers[questionId] !== undefined) return;

    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: selectedOptionIndex
    }));
  };

  return (
   <div className="quiz-wrapper">  {/* Ensures it takes full width of container */}
      
      {/* INPUT CARD */}
      <div className="input-card">
        <div className="input-group">
          <textarea
            className="styled-textarea"
            rows="6"
            placeholder="Paste your study notes or textbook content here (up to 2000 words)..."
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

      {/* ERROR DISPLAY */}
      {error && (
        <div className="error-box">
          <h3 className="error-title">{error.title}</h3>
          <p className="error-msg">{error.message}</p>
        </div>
      )}

      {/* QUIZ DISPLAY */}
      {quizData && quizData.questions && (
        <div className="quiz-container">
          <h2 className="topic-title">
            Topic: {quizData.topic}
          </h2>

          {quizData.questions.map((q, index) => {
            const selectedOptionIndex = selectedAnswers[q.id];
            const isAnswered = selectedOptionIndex !== undefined;

            // Determine Correct Index Logic (Handles "A. Answer" vs "Answer")
            let correctOptionIndex = -1;
            q.options.forEach((option, idx) => {
              const optionLetter = String.fromCharCode(65 + idx); // A, B, C...
              // Check various formats the AI might return
              const fullOption = `${optionLetter}. ${option}`;
              if (
                fullOption === q.answer || 
                option === q.answer || 
                fullOption.trim() === q.answer.trim()
              ) {
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
                      {isCorrect ? "✅ Correct!" : `❌ Incorrect.`}
                    </p>
                    {!isCorrect && <p className="answer-correct">Correct answer: {q.answer}</p>}
                    <p className="answer-explanation">💡 {q.explanation}</p>
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