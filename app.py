import streamlit as st
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
from fpdf import FPDF

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.qa_pairs = []
    st.session_state.finished = False

# Extract resume text
def extract_text_from_pdf(pdf_file):
    pdf = PdfReader(pdf_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# Generate next HR-style question
def generate_question(llm, resume, qa_history):
    prompt = PromptTemplate.from_template("""
You are a strict but friendly HR interviewer conducting a mock job interview.

Here is the candidate's resume:
{resume}

Here is the Q&A so far:
{qa_history}

Now ask the next question based on their resume and previous answers. One question only. Make it natural, contextual, and professional like a real HR.
""")
    chain = prompt | llm
    return chain.invoke({"resume": resume, "qa_history": qa_history})

# Evaluate the candidate
def evaluate_candidate(llm, qa_history):
    prompt = PromptTemplate.from_template("""
You are a professional HR evaluator. You have just finished a mock interview.

Here is the full Q&A history:
{qa_history}

Write an honest and professional evaluation:
- Mention strengths
- Point out areas for improvement
- Offer advice on how to improve
- End with a score out of 10 and a final hiring recommendation (YES, MAYBE, or NO)
Tone: Friendly but firm.
""")
    chain = prompt | llm
    return chain.invoke({"qa_history": qa_history})

# Generate evaluation PDF
def generate_pdf(qa_pairs, evaluation):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Mock Interview Report", ln=True, align='C')

    pdf.ln(10)
    for i, (q, a) in enumerate(qa_pairs, 1):
        pdf.multi_cell(0, 10, f"Q{i}: {q}")
        pdf.multi_cell(0, 10, f"A{i}: {a}")
        pdf.ln(5)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="HR Evaluation", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, evaluation)

    pdf.output("evaluation.pdf")

# UI Layout
st.title("HR Mock Interview System")
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    llm = Ollama(model="llama2")  # or "mistral", "llama2", etc.

    if not st.session_state.finished:
        if st.session_state.step == 0:
            st.write("Interview will begin. Please answer each question clearly.")
            question = generate_question(llm, resume_text, "")
            st.session_state.current_question = question
            st.session_state.step += 1

        st.write(f"Question {st.session_state.step}: {st.session_state.current_question}")
        user_answer = st.text_input("Your Answer:", key=f"answer_{st.session_state.step}")

        if user_answer:
            st.session_state.qa_pairs.append((st.session_state.current_question, user_answer))
            qa_history = "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.qa_pairs])
            next_q = generate_question(llm, resume_text, qa_history)
            st.session_state.current_question = next_q
            st.session_state.step += 1
            st.experimental_rerun()

        if st.session_state.step > 5:  # Change number of questions here
            st.session_state.finished = True

    if st.session_state.finished:
        st.success("Interview complete.")
        st.write("Generating HR evaluation...")

        qa_history = "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.qa_pairs])
        evaluation = evaluate_candidate(llm, qa_history)
        st.text_area("HR Evaluation", evaluation, height=300)

        generate_pdf(st.session_state.qa_pairs, evaluation)
        with open("evaluation.pdf", "rb") as f:
            st.download_button("Download Interview Report", f, file_name="interview_evaluation.pdf")
