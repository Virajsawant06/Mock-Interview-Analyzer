import { Link } from "react-router-dom";

function Home() {
    return (
        <div>
            <h1>Mock Interview Analyzer</h1>
            <Link to="/interview">
                <button>Start Interview</button>
            </Link>
        </div>
    );
}

export default Home;
