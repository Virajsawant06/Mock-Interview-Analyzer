import streamlit as st
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
from fpdf import FPDF
import time

# Page configuration
st.set_page_config(
    page_title="AI Mock Interview System",
    page_icon="👔",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .interview-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .question {
        background-color: black;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 4px solid #3b71ca;
    }
    .answer {
        background-color: black;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 4px solid #14a44d;
    }
    .evaluation {
        background-color: #fff;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-top: 25px;
    }
    .highlight {
        color: #3b71ca;
        font-weight: bold;
    }
    .stButton button {
        background-color: #3b71ca;
        color: white;
        font-weight: bold;
    }
    .download-btn button {
        background-color: #14a44d;
        color: white;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .progress-container {
        width: 100%;
        margin-bottom: 20px;
    }
    .progress-bar {
        height: 10px;
        background-color: #e9ecef;
        border-radius: 5px;
        margin-top: 5px;
    }
    .progress-fill {
        height: 100%;
        background-color: #3b71ca;
        border-radius: 5px;
        transition: width 0.5s ease-in-out;
    }
    .hr-avatar {
        width: 60px;
        height: 60px;
        background-color: #3b71ca;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        margin: 0 auto 20px auto;
    }
    .thinking {
        font-style: italic;
        color: #6c757d;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.qa_pairs = []
    st.session_state.finished = False
    st.session_state.resume_text = ""
    st.session_state.current_question = ""
    st.session_state.evaluation = ""
    st.session_state.max_questions = 5
    st.session_state.loading = False
    st.session_state.generating_question = False

# Extract resume text
def extract_text_from_pdf(pdf_file):
    pdf = PdfReader(pdf_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# Generate next HR-style question
def generate_question(resume, qa_history=""):
    llm = Ollama(model="mistral")
    options={"temperature": 0.2, "top_k": 40, "num_predict": 30}
    prompt = PromptTemplate.from_template("""
You are a strict but friendly HR interviewer conducting a mock job interview. 

Here is the candidate's resume:
{resume}

Here is the Q&A so far:
{qa_history}

Now ask the next question based on their resume and previous answers. Your questions should be:
                                          
1.Start easy ask for introduction and hobbies

2.Natural and conversational

3.Questions should not be too lengthy and moderate for user to understand

4.Relevant to their experience and skills mentioned in the resume

5.First few questions should be easy then increase the level

6.Follow up on interesting points from their previous answers

7.Include some behavioral questions to assess soft skills

8.Include some technical questions relevant to their field

9.Adapt based on their previous responses just like a real interview

Ask ONE QUESTION only. Make it natural, contextual, and professional like a real HR interviewer would.
Don't repeat questions that have already been asked. Dont take too long to process and ask questions
""")
    
    chain = prompt | llm
    return chain.invoke({"resume": resume, "qa_history": qa_history})

# Evaluate the candidate
def evaluate_candidate(resume, qa_history):
    llm = Ollama(model="mistral")
    options={"temperature": 0.2, "top_k": 40, "num_predict": 30}
    prompt = PromptTemplate.from_template("""
You are a professional HR evaluator. You have just finished a mock interview.

Here is the candidate's resume:
{resume}

Here is the full Q&A history:
{qa_history}

Write an honest and professional evaluation:
1. Mention specific strengths demonstrated in the interview
2. Point out areas for improvement with constructive feedback
3. Offer specific advice on how to improve interview performance
4. Evaluate their responses against the skills and experience in their resume
5. End with a score out of 10 and a final hiring recommendation (YES, MAYBE, or NO)

Format your evaluation with clear sections and bullet points where appropriate.
Tone: Professional, constructive, and helpful.
""")
    
    chain = prompt | llm
    return chain.invoke({"resume": resume, "qa_history": qa_history})

# Generate evaluation PDF
def generate_pdf(resume_text, qa_pairs, evaluation):
    pdf = FPDF()
    
    # Add title page
    pdf.add_page()
    pdf.set_font("Arial", 'B', size=24)
    pdf.cell(200, 20, txt="Mock Interview Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Generated on: {time.strftime('%Y-%m-%d')}", ln=True, align='C')
    pdf.ln(20)
    
    # Add resume section
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(200, 10, txt="Candidate Resume", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, resume_text)
    
    # Add interview transcript
    pdf.add_page()
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(200, 10, txt="Interview Transcript", ln=True)
    pdf.ln(10)
    
    for i, (q, a) in enumerate(qa_pairs, 1):
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt=f"Question {i}:", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, q)
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt=f"Answer {i}:", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, a)
        pdf.ln(10)

    # Add evaluation
    pdf.add_page()
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(200, 10, txt="HR Evaluation", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, evaluation)

    pdf.output("interview_evaluation.pdf")
    
    with open("interview_evaluation.pdf", "rb") as f:
        return f.read()

# Main UI
st.title("AI Mock Interview System")
st.markdown("### Practice your interview skills with our AI-powered HR interviewer")

# Progress bar
if st.session_state.step > 0 and not st.session_state.finished:
    progress = st.session_state.step / st.session_state.max_questions
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown(f'<p>Question {st.session_state.step} of {st.session_state.max_questions}</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {progress * 100}%;"></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Upload resume page
if st.session_state.step == 0:
    st.markdown("## Upload your resume to begin")
    st.markdown("Our AI interviewer will analyze your resume and ask relevant questions based on your experience.")
    
    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        max_q = st.slider("Number of interview questions:", min_value=3, max_value=10, value=5)
        st.session_state.max_questions = max_q
    
    if uploaded_file:
        if st.button("Start Interview"):
            with st.spinner("Analyzing your resume..."):
                st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
                st.session_state.step = 1
                st.session_state.generating_question = True
                st.rerun()

# Interview in progress
elif not st.session_state.finished:
    st.markdown("## Mock Interview")
    
    # Display interview progress
    st.markdown('<div class="interview-container">', unsafe_allow_html=True)
    
    # HR avatar
    st.markdown('<div class="hr-avatar">HR</div>', unsafe_allow_html=True)
    
    # Display QA history
    if len(st.session_state.qa_pairs) > 0:
        for i, (q, a) in enumerate(st.session_state.qa_pairs):
            st.markdown(f'<div class="question"><strong>HR:</strong> {q}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="answer"><strong>You:</strong> {a}</div>', unsafe_allow_html=True)
    
    # Generate question if needed
    if st.session_state.generating_question:
        st.markdown('<p class="thinking">HR is thinking of the next question...</p>', unsafe_allow_html=True)
        
        # Format QA history for the model
        qa_history = "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.qa_pairs])
        
        # Generate the next question
        with st.spinner(""):
            st.session_state.current_question = generate_question(st.session_state.resume_text, qa_history)
            st.session_state.generating_question = False
            st.rerun()
    
    # Display current question
    if st.session_state.current_question:
        st.markdown(f'<div class="question"><strong>HR:</strong> {st.session_state.current_question}</div>', unsafe_allow_html=True)
        
        # User answer input
        user_answer = st.text_area("Your Answer:", height=150, 
                                  placeholder="Type your answer here. Be professional and specific.")
        
        if st.button("Submit Answer"):
            if not user_answer:
                st.error("Please provide an answer before proceeding.")
            else:
                # Save current QA pair
                st.session_state.qa_pairs.append((st.session_state.current_question, user_answer))
                
                # Check if we've reached the maximum number of questions
                if len(st.session_state.qa_pairs) >= st.session_state.max_questions:
                    st.session_state.finished = True
                    
                    # Format QA history for evaluation
                    qa_history = "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.qa_pairs])
                    
                    # Show evaluation spinner
                    with st.spinner("Generating your interview evaluation..."):
                        st.session_state.evaluation = evaluate_candidate(st.session_state.resume_text, qa_history)
                else:
                    # Prepare for next question
                    st.session_state.current_question = ""
                    st.session_state.generating_question = True
                    st.session_state.step += 1
                
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Interview tips
    with st.expander("Interview Tips"):
        st.markdown("""
        - **Use the STAR method** for behavioral questions: Situation, Task, Action, Result
        - **Be specific** and provide concrete examples
        - **Keep your answers concise** but thorough (1-2 minutes per question)
        - **Stay positive** even when describing challenges
        - **Ask clarifying questions** if needed
        """)

# Evaluation page
else:
    st.markdown("## Interview Complete!")
    
    # Display evaluation
    st.markdown('<div class="evaluation">', unsafe_allow_html=True)
    st.markdown("### HR Evaluation")
    st.markdown(st.session_state.evaluation)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Transcript
    with st.expander("View Interview Transcript"):
        for i, (q, a) in enumerate(st.session_state.qa_pairs, 1):
            st.markdown(f"**Question {i}:** {q}")
            st.markdown(f"**Your Answer:** {a}")
            st.markdown("---")
    
    # Download report
    col1, col2 = st.columns(2)
    
    with col1:
        pdf_data = generate_pdf(st.session_state.resume_text, st.session_state.qa_pairs, st.session_state.evaluation)
        st.download_button(
            label="Download Interview Report (PDF)",
            data=pdf_data,
            file_name="interview_evaluation.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download-pdf"
        )
    
    with col2:
        if st.button("Start New Interview", use_container_width=True):
            # Reset session state
            st.session_state.step = 0
            st.session_state.qa_pairs = []
            st.session_state.finished = False
            st.session_state.resume_text = ""
            st.session_state.current_question = ""
            st.session_state.evaluation = ""
            st.session_state.generating_question = False
            st.rerun()