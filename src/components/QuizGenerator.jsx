import React, { useState } from 'react';
import { generateQuiz } from '../services/api';

const QuizGenerator = () => {
  const [inputText, setInputText] = useState('');
  const [topic, setTopic] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quizData, setQuizData] = useState(null);
  const [revealedAnswers, setRevealedAnswers] = useState({});

  const handleGenerate = async () => {
    // Reset states
    setError(null);
    setQuizData(null);
    setRevealedAnswers({});
    
    // UI Validation
    if (!inputText || !topic) {
      setError({ 
        title: "Missing Information", 
        message: "Please upload text and define a topic first." 
      });
      return;
    }

    setIsLoading(true);

    try {
      // Latency is approx 4.1s based on Aleksandre's audit
      const data = await generateQuiz(inputText, topic, "medium");
      setQuizData(data);
    } catch (err) {
      // User-Friendly Error Mapping
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

  const toggleAnswer = (questionId) => {
    setRevealedAnswers(prev => ({
      ...prev,
      [questionId]: !prev[questionId]
    }));
  };

  return (
    <div className="max-w-2xl mx-auto p-4 font-sans text-gray-800">
      {/* INPUT SECTION */}
      <div className="space-y-4 mb-8">
        <textarea
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
          rows="4"
          placeholder="Paste study material here..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <input
          type="text"
          className="w-full p-3 border border-gray-300 rounded-lg"
          placeholder="Topic (e.g., History, Python)"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        
        {/* GENERATE BUTTON WITH LOADING STATE */}
        <button
          onClick={handleGenerate}
          disabled={isLoading}
          className={`w-full py-3 px-6 rounded-lg text-white font-medium transition-all
            ${isLoading ? 'bg-indigo-300 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'}`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Generating Quiz (approx 4s)...
            </span>
          ) : (
            "Generate Study Quiz"
          )}
        </button>
      </div>

      {/* ERROR MESSAGE COMPONENT */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">{error.title}</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error.message}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* QUIZ DISPLAY */}
      {quizData && quizData.questions && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900 border-b pb-2">
            Topic: {quizData.topic}
          </h2>
          
          {quizData.questions.map((q, index) => (
            <div key={q.id || index} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <div className="flex items-start gap-3">
                <span className="bg-indigo-100 text-indigo-800 text-sm font-bold px-2.5 py-0.5 rounded">
                  Q{index + 1}
                </span>
                <h3 className="text-lg font-medium text-gray-900 mt-1">{q.question}</h3>
              </div>

              <div className="mt-4 grid gap-2">
                {q.options.map((option, idx) => (
                  <div key={idx} className="p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                    <span className="font-bold text-gray-400 mr-2">{String.fromCharCode(65 + idx)}.</span>
                    {option}
                  </div>
                ))}
              </div>

              <button
                onClick={() => toggleAnswer(q.id)}
                className="mt-4 text-sm text-indigo-600 font-medium hover:text-indigo-800"
              >
                {revealedAnswers[q.id] ? "Hide Answer" : "Show Answer"}
              </button>

              {revealedAnswers[q.id] && (
                <div className="mt-3 p-4 bg-green-50 rounded-lg border border-green-100 text-sm">
                  <p className="font-bold text-green-800">Correct Answer: {q.answer}</p>
                  <p className="text-green-700 mt-1">{q.explanation}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default QuizGenerator;
