import streamlit as st
import cohere
from dotenv import load_dotenv
import os

# Load .env key
load_dotenv()
COHERE_API_KEY = "GKVGjhN6t4MFCsDRtJdheYbT3xzq1QyVFarViQR7"  # Or use os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

# Streamlit page setup
st.set_page_config(page_title="PM JD Skill | Skills Extractor", page_icon="🧠")

# Tabs
tab1, tab2 = st.tabs(["📝 JD Skill Extractor", "📄 Resume Samples"])

# ---------- TAB 1: JD Skill Extractor ----------
with tab1:
    st.title("🧠 Product Manager JD Skill | Skills Extractor")
    st.markdown("Paste a job description, and we'll extract required skills **and** the best ATS keywords.")

    jd_text = st.text_area("📄 Paste PM Job Description Below", height=300)

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
                    skills_response = co.generate(
                        model='command',
                        prompt=skills_prompt,
                        max_tokens=250,
                        temperature=0.6
                    )
                    skills_output = skills_response.generations[0].text.strip()

                    ats_response = co.generate(
                        model='command',
                        prompt=ats_prompt,
                        max_tokens=100,
                        temperature=0.5
                    )
                    ats_keywords = ats_response.generations[0].text.strip()

                    st.success("✅ Skill Breakdown:")
                    st.markdown(skills_output)

                    st.divider()

                    st.success("🎯 ATS Keywords (for resume optimization):")
                    st.markdown(f"`{ats_keywords}`")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ---------- TAB 2: Resume Samples ----------
with tab2:
    st.title("📄 Sample Resumes for Product Managers")
    st.markdown("""
Here are a few resume formats tailored for Product Managers:""")

### ✅ Resume Sample 1: Classic PM Resume
