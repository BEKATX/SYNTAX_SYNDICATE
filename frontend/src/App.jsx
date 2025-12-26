import React from 'react';
import QuizGenerator from './components/QuizGenerator';
import './App.css'; 

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">🧠 COGNIFY</div>
          <div className="tagline">AI Study Assistant</div>
        </div>
      </header>

      <main className="container">
        <QuizGenerator />
      </main>
    </div>
  );
}

export default App;