import { useState, useEffect, useRef } from "react";
import Webcam from "react-webcam";
import axios from "axios";
import QuestionCard from "./questioncard";
import "./interview.css";
import { CheckCircle } from "lucide-react";

function Interview() {
    const [questions, setQuestions] = useState([]);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [emotion, setEmotion] = useState("Waiting...");
    const [answer, setAnswer] = useState("");
    const [isComplete, setIsComplete] = useState(false);
    const [answers, setAnswers] = useState([]);
    const webcamRef = useRef(null);

    // Fetch questions when component loads
    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/questions/")
            .then(response => setQuestions(response.data))
            .catch(error => {
                console.error("Error fetching questions:", error);
                // Fallback questions in case API fails
                setQuestions([
                    { id: 1, question: "Tell me about yourself and your background." },
                    { id: 2, question: "What are your greatest strengths?" },
                    { id: 3, question: "How do you handle stress and pressure?" }
                ]);
            });
    }, []);

    // Capture emotion every 2 seconds - KEEPING THIS EXACTLY AS THE ORIGINAL
    useEffect(() => {
        const interval = setInterval(() => {
            if (webcamRef.current) {
                captureFrame();
            }
        }, 2000);

        return () => clearInterval(interval);
    }, []);

    // Function to capture frame & send to Django API - KEEPING THIS EXACTLY AS THE ORIGINAL
    const captureFrame = async () => {
        if (!webcamRef.current) return;

        const imageSrc = webcamRef.current.getScreenshot();
        if (imageSrc) {
            try {
                const response = await axios.post("http://127.0.0.1:8000/api/emotion/", { image: imageSrc });
                setEmotion(response.data.emotion);
            } catch (error) {
                console.error("Error detecting emotion:", error);
            }
        }
    };

    // Handle answer submission
    const handleNextQuestion = () => {
        if (answer.trim() === "") {
            alert("Please provide an answer before proceeding.");
            return;
        }

        const newAnswers = [...answers];
        newAnswers[currentQuestionIndex] = answer;
        setAnswers(newAnswers);

        setAnswer("");  // Clear the input

        if (currentQuestionIndex < questions.length - 1) {
            setCurrentQuestionIndex(currentQuestionIndex + 1);
        } else {
            setIsComplete(true);
        }
    };

    // Handle previous question
    const handlePreviousQuestion = () => {
        if (currentQuestionIndex > 0) {
            setCurrentQuestionIndex(currentQuestionIndex - 1);
            setAnswer(answers[currentQuestionIndex - 1] || "");
        }
    };

    // Calculate progress percentage
    const progressPercentage = questions.length > 0 
        ? ((currentQuestionIndex + 1) / questions.length) * 100 
        : 0;

    // If interview is complete
    if (isComplete) {
        return (
            <div className="interview-container">
                <div className="interview-complete">
                    <div className="complete-icon">
                        <CheckCircle size={48} />
                    </div>
                    <h2 className="complete-heading">Interview Complete!</h2>
                    <p className="complete-message">
                        Great job! You've completed all the questions. 
                        Your responses have been recorded.
                    </p>
                    <button 
                        className="btn btn-primary" 
                        onClick={() => {
                            setIsComplete(false);
                            setCurrentQuestionIndex(0);
                            setAnswer("");
                        }}
                    >
                        Start New Interview
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="interview-container">
            <div className="interview-header">
                <h2>Mock Interview Practice</h2>
                <p>Answer each question while monitoring your facial expressions</p>
            </div>

            <div className="progress-bar">
                <div 
                    className="progress-fill" 
                    style={{ width: `${progressPercentage}%` }}
                ></div>
            </div>

            <div className="interview-content">
                {/* Webcam Section */}
                <div className="webcam-section">
                    <div className="section-header">
                        Facial Expression Analysis
                    </div>
                    <div className="section-content">
                        <div className="webcam-container">
                            <Webcam 
                                ref={webcamRef} 
                                screenshotFormat="image/jpeg"
                                width="100%"
                                height="auto"
                            />
                        </div>
                        <div className="blink-recording">
                            <div className="recording-dot"></div>
                            <span>Live Analysis</span>
                        </div>
                        <div className="emotion-display">
                            <div className="emotion-label">DETECTED EMOTION</div>
                            <div className="emotion-value">{emotion}</div>
                        </div>
                    </div>
                </div>
        
                {/* Questions Section */}
                <div className="question-section">
                    <div className="section-header">
                        Interview Questions ({currentQuestionIndex + 1}/{questions.length})
                    </div>
                    <div className="section-content">
                        {questions.length > 0 ? (
                            <div>
                                <QuestionCard 
                                    question={questions[currentQuestionIndex].question}
                                    questionNumber={currentQuestionIndex + 1}
                                />
                                <div className="question-input">
                                    <textarea
                                        className="answer-input"
                                        rows="5"
                                        value={answer}
                                        onChange={(e) => setAnswer(e.target.value)}
                                        placeholder="Type your answer here..."
                                    />
                                    <div className="button-group">
                                        <button 
                                            className="btn btn-secondary"
                                            onClick={handlePreviousQuestion}
                                            disabled={currentQuestionIndex === 0}
                                        >
                                            Previous
                                        </button>
                                        <button 
                                            className="btn btn-primary"
                                            onClick={handleNextQuestion}
                                        >
                                            {currentQuestionIndex < questions.length - 1 ? "Next Question" : "Complete Interview"}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <p>Loading questions...</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Interview;