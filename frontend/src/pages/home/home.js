import { Link } from "react-router-dom";
import { Video, Smile, ArrowRight, Award, Lightbulb, BarChart } from "lucide-react";
import "./home.css";

function Home() {
  return (
    <div className="home-container">
      <div className="home-header">
        <h1>Mock Interview Analyzer</h1>
        <p>Improve your interview skills with real-time feedback on your facial expressions and responses</p>
        <Link to="/interview" className="btn btn-primary">
          Start Practice Interview <ArrowRight size={20} className="btn-icon" />
        </Link>
      </div>

      <div className="features-grid">
        <div className="feature-card">
          <div className="feature-icon">
            <Video size={32} />
          </div>
          <h3>Webcam Analysis</h3>
          <p>Our AI analyzes your facial expressions in real-time during the interview practice</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <Smile size={32} />
          </div>
          <h3>Emotion Detection</h3>
          <p>Get instant feedback on how your emotions are perceived during your responses</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <BarChart size={32} />
          </div>
          <h3>Performance Tracking</h3>
          <p>Track your progress over time and see how your interview skills improve</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <Lightbulb size={32} />
          </div>
          <h3>Personalized Tips</h3>
          <p>Receive customized advice based on your performance and response patterns</p>
        </div>
      </div>

      <div className="how-it-works">
        <h2>How It Works</h2>
        <div className="steps-container">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Start a Practice Session</h3>
            <p>Choose from our library of common interview questions or create a custom session</p>
          </div>
          
          <div className="step">
            <div className="step-number">2</div>
            <h3>Answer Questions</h3>
            <p>Respond to questions while our AI analyzes your facial expressions and confidence</p>
          </div>
          
          <div className="step">
            <div className="step-number">3</div>
            <h3>Review Feedback</h3>
            <p>Get detailed insights on your performance and areas for improvement</p>
          </div>
        </div>
      </div>

      <div className="cta-section">
        <div className="cta-content">
          <h2>Ready to ace your next interview?</h2>
          <p>Start practicing now and build your confidence with real-time feedback</p>
          <Link to="/interview" className="btn btn-primary">
            Begin Practice <ArrowRight size={20} className="btn-icon" />
          </Link>
        </div>
        <div className="testimonial">
          <div className="quote">"This tool helped me overcome my interview anxiety and land my dream job!"</div>
          <div className="author">- Sarah J., Software Engineer</div>
        </div>
      </div>
    </div>
  );
}

export default Home;