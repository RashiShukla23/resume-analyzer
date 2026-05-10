# Resume Analyzer

A tool that reads your resume and gives structured feedback using GPT-4.1. Upload a PDF, paste a job description, and get a breakdown of your strengths, gaps, and what to improve — in seconds.

---

## What it does

- Extracts text from resume PDFs using LangChain's PDF loader
- Matches your resume against a job description you provide
- Returns feedback in structured JSON format every time
- Uses few-shot prompting to keep the analysis consistent and detailed

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | GPT-4.1 (OpenAI) |
| Framework | LangChain |
| PDF Parsing | LangChain PDF Loader |
| Frontend | Streamlit |
| Output Format | Structured JSON |
| Language | Python |

---

## Project Structure

```
resume-analyzer/
├── app.py       # Streamlit UI + LangChain pipeline
└── .gitignore
```

---

## Getting Started

Prerequisites: Python 3.10+, OpenAI API key

```bash
git clone https://github.com/RashiShukla23/resume-analyzer.git
cd resume-analyzer

py -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```
OPENAI_API_KEY=your_key
```

```bash
streamlit run app.py
```

---

## How it works

The resume PDF is loaded and parsed by LangChain. The extracted text along with the job description is sent to GPT-4.1 with a few-shot system prompt that instructs the model to return structured JSON feedback. The result is displayed directly in the Streamlit UI.

---

## Sample Output

```json
{
  "overall_score": 78,
  "strengths": [
    "Strong project section with real tech stack",
    "Clear education background"
  ],
  "gaps": [
    "No quantified impact in project descriptions",
    "Missing relevant keywords for the role"
  ],
  "suggestions": [
    "Add metrics to project outcomes",
    "Include internship or open source experience"
  ],
  "job_match": "Medium — 3 out of 6 required skills found"
}
```

---

## Author

**Rashi Shukla** — [GitHub](https://github.com/RashiShukla23)
