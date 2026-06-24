# ⚡ PitchLens AI

An AI-powered pitch deck evaluator that analyzes startup presentations 
through the lens of a venture capitalist.

## What it does

Upload a pitch deck PDF and get a structured investor-grade evaluation across three dimensions:

- **Communication (30%)** — clarity, readability, information density
- **Narrative (30%)** — logical flow, storytelling, missing sections
- **Problem-Solution Fit (40%)** — problem significance, solution relevance, venture scalability

## Output

- Overall score out of 100
- Verdict (Strong Opportunity / Worth Further Diligence / Needs Work / Not Investment Ready)
- Per-dimension scores with strengths and weaknesses
- Top investor risks
- Due diligence questions an investor would ask

## Tech Stack

- Python 3.11
- Streamlit — frontend
- pdfplumber — PDF text extraction
- Groq API (LLaMA-3.3-70B) — evaluation engine

## Project Structure
pitch-deck-evaluator/

│

├── app.py                  # Streamlit frontend

├── requirements.txt

├── .env                    # GROQ_API_KEY (not committed)

│

├── modules/
│     ├── pdf_parser.py     # Extract text from PDF

│     ├── evaluator.py      # LLM evaluation logic

│     ├── prompts.py        # VC-calibrated prompt engineering

│     └── report.py         # Score interpretation and report packaging

│

└── sample_decks/           # Test decks

## Setup

```bash
git clone https://github.com/amanighribi/pitch-deck-evaluator
cd pitch-deck-evaluator
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
GROQ_API_KEY=your_key_here

Run the app:
```bash
streamlit run app.py
```

## Design Decisions

- **LLaMA-3.3-70B via Groq** — fast inference, free tier, strong reasoning capability
- **temperature=0.3** — low temperature for consistent, focused evaluation output
- **Structured JSON output** — makes scores easy to parse and display reliably
- **30/30/40 weighting** — Problem-Solution Fit carries the most weight because it's 
  the strongest predictor of venture potential at early stage