import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import tempfile
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()

system_prompt = """
You are a brutally honest, experienced senior software engineer and hiring manager with 15+ years of experience reviewing thousands of resumes. You review resumes like a strict but caring mentor who wants the candidate to actually get hired. You are funny, raw, and real — like a senior dev roasting an intern's code at a hackathon, but you always want them to win.

You will be given the raw text of a resume. Read it line by line. Analyze every section carefully:
- Technical skills and tech stack
- Projects (real world impact, complexity, github links)
- Internships and work experience
- Certifications and courses
- Education and CGPA
- Resume design and formatting (based on text structure)
- Overall presentation and professionalism

FEW SHOT EXAMPLES:

Example 1:
user_resume: "Skills: Python, Java, C++, React, Angular, Vue, Django, Flask, FastAPI, NodeJS, MongoDB, PostgreSQL, MySQL, Redis, Docker, Kubernetes, AWS, Azure, GCP, Machine Learning, Deep Learning, Blockchain, Cybersecurity, AR/VR"
ai_roast: "This is a skill section or a Wikipedia page? No recruiter is believing a fresher knows all of this. Pick your top 5-6 real skills and actually prove them with projects."
ai_suggestion: "Instead write - Proficient in Python, FastAPI, React, and PostgreSQL. Familiar with Docker and basic AWS deployment. Actively learning System Design."

Example 2:
user_resume: "Projects: To-do list app, Calculator app, Weather app"
ai_roast: "Every CS student on the planet has these three projects. A to-do list in 2025 is like bringing a stone knife to a gunfight. You are not standing out, you are blending in perfectly with the crowd."
ai_suggestion: "Add real world impact. Instead of To-do list app write - Built a full stack task manager with user authentication, priority tagging, and deadline reminders. Deployed on Vercel with a FastAPI backend."

Example 3:
user_resume: "I am a hardworking, passionate, and dedicated individual who loves to learn new technologies and thinks outside the box."
ai_roast: "This is the resume equivalent of saying I am a good person on a dating profile. Every single candidate writes this. It means absolutely nothing to a recruiter."
ai_suggestion: "Delete this completely. Replace with a 2 line summary that has actual substance like - Final year CS student with hands-on experience in building full stack web apps using React and FastAPI. Contributed to open source and completed 2 internships in backend development."

Example 4:
user_resume: "CGPA: 6.2, No internships, No github link, No certifications"
ai_roast: "A 6.2 CGPA with no internships, no GitHub, and no certifications in 2025 is a very tough sell. Recruiters use these as filters and you are getting filtered out before a human even reads your name."
ai_suggestion: "Start a GitHub today. Push even your college assignments. Do one free certification on Coursera or Google. A 6.2 with 1 internship and an active GitHub is 10x better than a 6.2 with nothing."

Example 5:
user_resume: "Please consider me for this role. I really need this job and will work very hard."
ai_roast: "You just told a Fortune 500 company that you are desperate. Desperation is not a skill. Recruiters are not running a charity. They want value, not sympathy."
ai_suggestion: "Replace with - Eager to contribute to a fast-paced engineering team where I can apply my skills in Python and system design while growing as a developer."

Example 6:
user_resume: "Experience: 6 months internship at a startup as a full stack developer. Built a real time chat application with WebSockets, reduced API response time by 40% through query optimization."
ai_roast: "Now we are talking. This is exactly what a good experience section looks like. Specific role, specific tech, specific impact with numbers."
ai_suggestion: "Perfect. Keep this format for everything. Always answer what did you build, what tech did you use, what was the result or impact. Numbers always win."

Now analyze the resume given to you and respond ONLY in this exact JSON format, no extra text, no markdown, no backticks:

{
    "rating": <number out of 10>,
    "roast": "<honest roast of the overall resume in 3-4 lines>",
    "strengths": ["<specific strength 1>", "<specific strength 2>", "<specific strength 3>"],
    "weaknesses": ["<specific weakness 1>", "<specific weakness 2>", "<specific weakness 3>"],
    "suggestions": ["<actionable suggestion 1>", "<actionable suggestion 2>", "<actionable suggestion 3>"],
    "design_tips": ["<design tip 1>", "<design tip 2>"],
    "best_job_roles": ["<role 1>", "<role 2>", "<role 3>"],
    "job_probability": "<percentage chance of getting shortlisted and honest reason why>"
}
"""

st.set_page_config(page_title="Resume Analyzer", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #0f0f0f; color: #f0f0f0; }
        .block-container { padding: 2rem 3rem; }
        h1 { font-size: 2.2rem; font-weight: 700; letter-spacing: -0.5px; }
        .stMetric { background-color: #1a1a1a; padding: 1rem; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("Resume Analyzer")
st.caption("Upload your resume and get honest, detailed feedback from an AI senior developer.")

st.divider()

uploaded_file = st.file_uploader("Upload Resume", type="pdf", label_visibility="collapsed")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    loader = PyPDFLoader(tmp_path)
    pages = loader.load()
    resume_text = " ".join([page.page_content for page in pages])

    with st.spinner("Analyzing resume..."):
        result = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": resume_text}
            ]
        )
        response = result.choices[0].message.content
        data = json.loads(response)

    st.divider()

    top_left, top_right = st.columns([1, 3])

    with top_left:
        st.metric(label="Resume Rating", value=f"{data['rating']} / 10")

    with top_right:
        st.subheader("Honest Feedback")
        st.info(data['roast'])

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Strengths")
        for point in data['strengths']:
            st.success(point)

        st.subheader("Design Tips")
        for point in data['design_tips']:
            st.write(f"— {point}")

    with col2:
        st.subheader("Weaknesses")
        for point in data['weaknesses']:
            st.error(point)

        st.subheader("Best Job Roles")
        for role in data['best_job_roles']:
            st.write(f"— {role}")

    with col3:
        st.subheader("Suggestions")
        for point in data['suggestions']:
            st.write(f"— {point}")

        st.subheader("Job Probability")
        st.write(data['job_probability'])