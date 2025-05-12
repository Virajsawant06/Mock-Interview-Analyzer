# Mock Interview Analyzer (Django Version)

## Project Overview

The Mock Interview Analyzer is a web-based application designed to help students practice job interviews by analyzing their facial expressions. The system records the user's emotions in real-time and generates a comprehensive report, helping users improve their interview skills.

## Features

* Real-time emotion analysis during mock interviews.
* Automated emotion recording every 2 seconds.
* Step-by-step interview question display.
* AI-generated reports using recorded emotions and interview answers.
* Emotion data storage in MongoDB.
* User-friendly interface with React.

## Project Structure

* **Backend (Django)**: Manages emotion analysis, data processing, and database interactions.
* **Frontend (React)**: Provides an interactive UI for conducting interviews.
* **Database (MongoDB)**: Stores recorded emotion data with timestamps.
* **AI Report Generation**: Uses AI to generate feedback from the collected data.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/username/mock-interview-analyzer.git
   cd mock-interview-analyzer
   ```

2. Install backend dependencies:

   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   ```

3. Install frontend dependencies:

   ```bash
   cd frontend
   npm install
   ```

4. Start the backend server:

   ```bash
   python manage.py runserver
   ```

5. Start the frontend server:

   ```bash
   npm start
   ```

## Usage

1. Open the application in your web browser.
2. Start a new interview session.
3. Answer the questions as they appear one by one.
4. View real-time emotion analysis on the screen.
5. After the interview, review the AI-generated report.

## Technologies Used

* **Python**: Backend logic and deep learning model integration.
* **Django**: Web framework for backend operations.
* **React**: Frontend framework for user interactions.
* **MongoDB**: Database for storing emotion data.
* **OpenCV**: Face and emotion detection.
* **Machine Learning**: Custom model for emotion recognition.
* **Gemini AI**: AI-based report generation.

## Future Enhancements

* Incorporating voice analysis for deeper insights.
* Customizable question sets for different interview scenarios.
* Enhanced accuracy for emotion detection.

## Contributing

Contributions are welcome! Fork the repository, make improvements, and submit a pull request.

## License

This project is licensed under the MIT License.
