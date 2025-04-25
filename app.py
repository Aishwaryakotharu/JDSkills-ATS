import streamlit as st
import cohere
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY") or "GKVGjhN6t4MFCsDRtJdheYbT3xzq1QyVFarViQR7"
co = cohere.Client(COHERE_API_KEY)

# Page configuration
st.set_page_config(page_title="PM JD Skill | Skills Extractor", page_icon="🧠")

# Define tabs
tab1, tab2 = st.tabs(["📝 JD Skill Extractor", "📄 Resume Samples"])

# ---------------- Tab 1: JD Skill + ATS Extractor ----------------
with tab1:
    st.title("🧠 Product Manager JD Skill | Skills Extractor")
    st.markdown("Paste a job description, and we'll extract required skills **and** the best ATS keywords.")

    jd_text = st.text_area("📄 Paste PM Job Description Below", height=300)

    if st.button("🔍 Extract Skills + ATS Keywords"):
        if not jd_text.strip():
            st.warning("⚠️ Please paste a job description first.")
        else:
            with st.spinner("Analyzing with Cohere..."):
                skills_prompt = f"""
You are a career coach and hiring expert.

From the following Product Manager job description, extract:
- Required skills (must-have)
- Nice-to-have skills (optional)

Format each as a bullet point list.

Job Description:
{jd_text}
"""

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

# ---------------- Tab 2: Resume Samples ----------------
with tab2:
    st.title("📄 Sample Resumes for Product Managers")

    st.markdown("""
Need inspiration for your PM resume? Check out these examples:

### ✅ Sample Resume 1: Classic PM Style
Name: Jane Doe
Title: Senior Product Manager
Email: jane.doe@email.com
LinkedIn: linkedin.com/in/janedoe

🔹 SUMMARY
Innovative Product Manager with 7+ years of experience leading cross-functional teams...

🔹 SKILLS

Roadmapping, A/B Testing, Agile/Scrum

SQL, Figma, JIRA, Google Analytics

🔹 EXPERIENCE
Product Manager, Acme Corp (2020–2024)

Led end-to-end development of X platform...

🔹 EDUCATION
B.S. in Computer Science, XYZ University


### ✅ Downloadable Resume Template

We’ve also included a professional Word document (.docx) template you can customize.
""")

    try:
        with open("/mnt/data/2024-template_bullet.docx", "rb") as file:
            st.download_button(
                label="📥 Download Resume Template (.docx)",
                data=file,
                file_name="PM_Resume_Template.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    except FileNotFoundError:
        st.warning("⚠️ Resume template not found. Please upload the file to `/mnt/data/`.")

    st.markdown("""
---

Need more samples or want to upload your resume for feedback? Let us know below!
""")

