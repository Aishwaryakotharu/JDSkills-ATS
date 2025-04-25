import streamlit as st
import cohere
from dotenv import load_dotenv
import os

# Load .env key
load_dotenv()
COHERE_API_KEY = "GKVGjhN6t4MFCsDRtJdheYbT3xzq1QyVFarViQR7"  # You can also load with os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

# Streamlit page setup
st.set_page_config(page_title="PM JD Skill| SKills Extractor", page_icon="🧠")
st.title("🧠 Product Manager JD Skill | Skills Extractor")
st.markdown("Paste a job description, and we'll extract required skills **and** the best ATS keywords.")

# Text area input
jd_text = st.text_area("📄 Paste PM Job Description Below", height=300)

# Button
if st.button("🔍 Extract Skills + ATS Keywords"):
    if not jd_text.strip():
        st.warning("⚠️ Please paste a job description first.")
    else:
        with st.spinner("Analyzing with Cohere..."):

            # Prompt 1: Extract skills
            skills_prompt = f"""
You are a career coach and hiring expert.

From the following Product Manager job description, extract:
- Required skills (must-have)
- Nice-to-have skills (optional)

Format each as a bullet point list.

Job Description:
{jd_text}
"""

            # Prompt 2: Extract ATS-friendly keywords
            ats_prompt = f"""
From the following Product Manager job description, extract a list of ATS-friendly keywords that would help a resume get picked by a recruiter or applicant tracking system.

List up to 15 relevant keywords and tools, as comma-separated values.

Job Description:
{jd_text}
"""

            try:
                # Response 1: Skill breakdown
                skills_response = co.generate(
                    model='command',
                    prompt=skills_prompt,
                    max_tokens=250,
                    temperature=0.6
                )
                skills_output = skills_response.generations[0].text.strip()

                # Response 2: ATS keywords
                ats_response = co.generate(
                    model='command',
                    prompt=ats_prompt,
                    max_tokens=100,
                    temperature=0.5
                )
                ats_keywords = ats_response.generations[0].text.strip()

                # Display
                st.success("✅ Skill Breakdown:")
                st.markdown(skills_output)

                st.divider()

                st.success("🎯 ATS Keywords (for resume optimization):")
                st.markdown(f"`{ats_keywords}`")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

