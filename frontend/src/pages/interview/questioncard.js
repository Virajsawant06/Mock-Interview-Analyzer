import React from "react";

function QuestionCard({ question, questionNumber }) {
    return (
        <div className="question-card">
            <div className="question-number">{questionNumber}</div>
            <h3 className="question-text">{question}</h3>
        </div>
    );
}

export default QuestionCard;