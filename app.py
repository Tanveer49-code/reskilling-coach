import streamlit as st
import requests
import os
import json

st.set_page_config(
    page_title="AI Job-Displacement & Reskilling Coach",
    page_icon="🧭",
    layout="centered",
)

st.title("🧭 AI Job-Displacement & Reskilling Coach")
st.write(
    "Find out how exposed your job is to AI automation — and get a "
    "personalized plan to stay ahead."
)

# Load API key from Streamlit secrets (for deployed apps) or environment variable (for local runs)
api_key = None
try:
    api_key = st.secrets.get("GROQ_API_KEY", None)
except Exception:
    pass
if not api_key:
    api_key = os.environ.get("GROQ_API_KEY")

with st.form("job_form"):
    job_title = st.text_input(
        "Your job title",
        placeholder="e.g. Customer Support Representative",
    )
    tasks = st.text_area(
        "Briefly describe your daily tasks",
        placeholder="e.g. I answer customer emails, process refunds, "
        "update spreadsheets, and follow a script for common issues...",
        height=120,
    )
    submitted = st.form_submit_button("Analyze My Job", use_container_width=True)


def build_prompt(job_title: str, tasks: str) -> str:
    return f"""You are a career coach specializing in AI's impact on the job market.

A user has the following job:
Job Title: {job_title}
Daily Tasks: {tasks}

Analyze how exposed this job is to AI automation in the next 2-3 years, and
respond ONLY in valid JSON with this exact structure:

{{
  "risk_level": "Low" | "Medium" | "High",
  "risk_explanation": "2-3 sentence plain-language explanation of why, referencing their specific tasks",
  "reskilling_recommendations": [
    {{"skill": "skill name", "why": "1 sentence on why this skill helps them specifically"}},
    {{"skill": "skill name", "why": "..."}},
    {{"skill": "skill name", "why": "..."}}
  ],
  "next_steps": ["short actionable step 1", "short actionable step 2", "short actionable step 3"]
}}

Return ONLY the JSON object. No preamble, no markdown formatting, no code fences."""


def parse_json_response(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned.strip())


if submitted:
    if not job_title or not tasks:
        st.warning("Please fill in both fields.")
    elif not api_key:
        st.error(
            "No API key found. Set the GROQ_API_KEY environment variable "
            "(locally) or add it to Streamlit secrets (when deployed)."
        )
    else:
        with st.spinner("Analyzing your role..."):
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "openai/gpt-oss-120b",
                        "max_tokens": 1000,
                        "messages": [
                            {"role": "user", "content": build_prompt(job_title, tasks)}
                        ],
                    },
                    timeout=30,
                )
                response.raise_for_status()
                raw_text = response.json()["choices"][0]["message"]["content"]
                data = parse_json_response(raw_text)

                risk = data.get("risk_level", "Unknown")
                colors = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                st.subheader(f"{colors.get(risk, '⚪')} Risk Level: {risk}")
                st.write(data.get("risk_explanation", ""))

                st.markdown("### 📚 Recommended Skills to Learn")
                for rec in data.get("reskilling_recommendations", []):
                    st.markdown(f"**{rec.get('skill', '')}** — {rec.get('why', '')}")

                st.markdown("### ✅ Next Steps")
                for step in data.get("next_steps", []):
                    st.markdown(f"- {step}")

            except json.JSONDecodeError:
                st.error(
                    "Couldn't parse the AI's response. Please try again — "
                    "this can happen occasionally with model output."
                )
            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.markdown("---")
st.caption("Built for PakAngels GenAI & Agentic AI Training — Cohort 11 Hackathon")
