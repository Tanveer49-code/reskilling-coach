# 🧭 AI Job-Displacement & Reskilling Coach

A GenAI hackathon project (PakAngels Cohort 11) that helps users understand how
exposed their job is to AI automation, and gives them a personalized reskilling
plan.

## How it works
1. User enters their job title and a short description of their daily tasks.
2. The app sends this to Claude (Anthropic's LLM) with a structured prompt.
3. Claude returns a risk level (Low/Medium/High), an explanation, 3 personalized
   skill recommendations, and concrete next steps.

## 1. Get a free API key (Groq — no credit card needed)
Go to [console.groq.com/keys](https://console.groq.com/keys), sign up with an
email or Google account, and create a new key. It's genuinely free — no
credit card, no billing setup required.

## 2. Run it locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key (Mac/Linux)
export GROQ_API_KEY="your-key-here"

# Set your API key (Windows Command Prompt)
set GROQ_API_KEY=your-key-here

# Set your API key (Windows PowerShell)
$env:GROQ_API_KEY="your-key-here"

# Run the app
streamlit run app.py
```

It'll open automatically at `http://localhost:8501`.

## 3. Deploy it for free (you need a live link for submission)

The easiest option is **Streamlit Community Cloud**:

1. Push this folder to a public GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select your repo and `app.py` as the entry point.
4. Under **Advanced settings → Secrets**, add:
   ```
   GROQ_API_KEY = "your-key-here"
   ```
5. Click **Deploy**. You'll get a public URL like
   `https://your-app-name.streamlit.app` — that's your submission link.

## Files
- `app.py` — the Streamlit app
- `requirements.txt` — Python dependencies
- `README.md` — this file

## Notes for your pitch/demo video
- **Problem:** AI adoption is outpacing most workers' ability to adapt, and
  generic "AI will replace jobs" articles don't help anyone make a real decision.
- **Solution:** A personalized coach that assesses real automation risk based
  on someone's actual tasks, and gives them a concrete plan — not vague advice.
- **Tech stack:** Streamlit (frontend) + Groq API (Llama 3.3 70B) for the
  reasoning engine.
- **Architecture:** User input → prompt built with task context → Groq API
  call → structured JSON response → rendered in the UI.
