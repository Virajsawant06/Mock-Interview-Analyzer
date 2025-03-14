import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/home/home"; // Adjust this path to where your home.js file is actually located
import Interview from "./pages/interview/interview"; // Adjust this path to where your interview.js file is located
import Results from "./pages/results/results"; // Keep as is if this path is correct
import Report from "./report"; // Keep as is if this path is correct

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Navigate to="/home" />} /> {/* Redirect root to home */}
                <Route path="/home" element={<Home />} />
                <Route path="/interview" element={<Interview />} />
                <Route path="/results" element={<Results />} />
                <Route path="/report" element={<Report />} />
            </Routes>
        </Router>
    );
}

export default App;