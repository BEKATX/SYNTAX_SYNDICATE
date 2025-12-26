import React, { useState, useRef } from 'react';
import { generateQuiz, generateSummary, generateGlossary, uploadPDF } from '../services/api';

const QuizGenerator = () => {
  const [inputText, setInputText] = useState('');
  const [topic, setTopic] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quizData, setQuizData] = useState(null);
  const [summaryData, setSummaryData] = useState(null);
  const [glossaryData, setGlossaryData] = useState(null);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [activeTab, setActiveTab] = useState('quiz'); // 'summary', 'glossary', 'quiz'
  const fileInputRef = useRef(null);

  const handlePDFUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsLoading(true);
    setError(null);

    try {
      const result = await uploadPDF(file);
      if (result.success) {
        setInputText(result.extracted_text);
        setError({
          title: "PDF Uploaded Successfully",
          message: `Extracted text from ${result.page_count} page(s). Please set a topic and generate your study materials.`
        });
      }
    } catch (err) {
      setError({
        title: "PDF Upload Failed",
        message: err.message || "Could not extract text from PDF."
      });
    } finally {
      setIsLoading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleGenerate = async () => {
    setError(null);
    setQuizData(null);
    setSummaryData(null);
    setGlossaryData(null);
    setSelectedAnswers({});

    if (!inputText.trim() || !topic.trim()) {
      setError({
        title: "Missing Information",
        message: "Please provide text and define a topic first."
      });
      return;
    }

    setIsLoading(true);

    try {
      // Generate all three types of content
      const [quizResult, summaryResult, glossaryResult] = await Promise.all([
        generateQuiz(inputText, topic, "medium"),
        generateSummary(inputText, topic),
        generateGlossary(inputText, topic)
      ]);

      if (!quizResult || !quizResult.questions) {
        throw new Error("Invalid quiz format received from AI");
      }
      if (!summaryResult || !summaryResult.summary) {
        throw new Error("Invalid summary format received from AI");
      }
      if (!glossaryResult || !glossaryResult.terms) {
        throw new Error("Invalid glossary format received from AI");
      }

      setQuizData(quizResult);
      setSummaryData(summaryResult);
      setGlossaryData(glossaryResult);
    } catch (err) {
      if (err.message === "SERVICE_AT_CAPACITY") {
        setError({
          title: "Service at Capacity",
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
   <div className="quiz-wrapper">

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

        {/* PDF Upload Button */}
        <div className="input-group">
          <input
            type="file"
            ref={fileInputRef}
            accept=".pdf"
            onChange={handlePDFUpload}
            style={{ display: 'none' }}
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isLoading}
            className="pdf-upload-btn"
          >
            Upload PDF
          </button>
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
              Generating Study Materials...
            </>
          ) : (
            "Generate Study Materials"
          )}
        </button>
      </div>

      {/* LOADING OVERLAY */}
      {isLoading && (
        <div className="loading-overlay">
          <div className="loading-content">
            <div className="large-spinner"></div>
            <p className="loading-text">Generating your study materials...</p>
            <p className="loading-subtext">This may take 5-8 seconds</p>
          </div>
        </div>
      )}

      {/* ERROR DISPLAY */}
      {error && (
        <div className={`error-box ${error.title.includes("Success") ? "success-box" : ""}`}>
          <h3 className="error-title">{error.title}</h3>
          <p className="error-msg">{error.message}</p>
        </div>
      )}

      {/* TABS */}
      {(quizData || summaryData || glossaryData) && (
        <div className="tabs-container">
          <button
            className={`tab-btn ${activeTab === 'summary' ? 'active' : ''}`}
            onClick={() => setActiveTab('summary')}
            disabled={!summaryData}
          >
            Summary
          </button>
          <button
            className={`tab-btn ${activeTab === 'glossary' ? 'active' : ''}`}
            onClick={() => setActiveTab('glossary')}
            disabled={!glossaryData}
          >
            Glossary
          </button>
          <button
            className={`tab-btn ${activeTab === 'quiz' ? 'active' : ''}`}
            onClick={() => setActiveTab('quiz')}
            disabled={!quizData}
          >
            Quiz
          </button>
        </div>
      )}

      {/* SUMMARY VIEW */}
      {activeTab === 'summary' && summaryData && (
        <div className="summary-container">
          <h2 className="topic-title">Summary: {summaryData.topic}</h2>
          <div className="summary-content">
            <p>{summaryData.summary}</p>
          </div>
        </div>
      )}

      {/* GLOSSARY VIEW */}
      {activeTab === 'glossary' && glossaryData && (
        <div className="glossary-container">
          <h2 className="topic-title">Glossary: {glossaryData.topic}</h2>
          <div className="glossary-terms">
            {glossaryData.terms.map((term, index) => (
              <div key={index} className="glossary-item">
                <h3 className="glossary-term">{term.term}</h3>
                <p className="glossary-definition">{term.definition}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* QUIZ DISPLAY */}
      {activeTab === 'quiz' && quizData && quizData.questions && (
        <div className="quiz-container">
          <h2 className="topic-title">
            Quiz: {quizData.topic}
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