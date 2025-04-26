import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# Define paths for storing feedback and tracker data
feedback_path = "user_feedback.csv"
tracker_path = "application_tracker.csv"

# Create directories and files if they don't exist
os.makedirs("outputs", exist_ok=True)
os.makedirs("data", exist_ok=True)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="JD Skill Extractor", page_icon="🧠", layout="wide")

# Horizontal Tabs
tab1, tab2, tab3 = st.tabs(["📝 JD Skill Extractor", "📄 Resume Samples", "💬 Feedback & Discussion Board"])

# ---------------- Tab 1: JD Skill + ATS Extractor ----------------
with tab1:
    st.title("🧠 Product Manager JD Skill | Skills Extractor")
    st.markdown("Paste a job description, and we'll extract required skills **and** the best ATS keywords.")

    jd_text = st.text_area("📄 Paste PM Job Description Below", height=300)

    if st.button("🔍 Extract Skills + ATS Keywords"):
        if not jd_text.strip():
            st.warning("⚠️ Please paste a job description first.")
        else:
            with st.spinner("Analyzing..."):
                # Example placeholder for extracting skills and ATS keywords
                skills_output = "• Product Management\n• Agile\n• Roadmapping"
                ats_keywords = "Agile, Product Management, Roadmapping, Jira, Scrum"
                
                st.success("✅ Skill Breakdown:")
                st.markdown(skills_output)

                st.divider()

                st.success("🎯 ATS Keywords (for resume optimization):")
                st.markdown(f"`{ats_keywords}`")


# ---------------- Tab 2: Resume Samples ----------------
with tab2:
    st.title("📄 Sample Resumes for Product Managers")

    st.markdown("""---
### ✅ Sample Resume 1: Classic PM Style

**Name:** Jane Doe  
**Title:** Senior Product Manager  
**Email:** jane.doe@email.com  
**LinkedIn:** linkedin.com/in/janedoe

---
""")

    try:
        image = Image.open("PMResume.jpg")
        base_width = 700
        w_percent = base_width / float(image.size[0])
        h_size = int((float(image.size[1]) * float(w_percent)))
        resized_image = image.resize((base_width, h_size // 2))
        st.image(resized_image, caption="📄 PM Resume Template Preview", width=base_width)
    except FileNotFoundError:
        st.warning("⚠️ Resume image not found. Make sure 'PMResume.jpg' is in the same folder.")

    st.markdown("""
---

### ✅ Downloadable Resume Template

We’ve also included a professional Word document (.docx) template you can customize.
""")

    try:
        with open("2024-template_bullet.docx", "rb") as file:
            st.download_button(
                label="📥 Download Resume Template (.docx)",
                data=file,
                file_name="PM_Resume_Template.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="download_resume_docx_tab2"
            )
    except FileNotFoundError:
        st.warning("⚠️ Resume template not found. Please ensure '2024-template_bullet.docx' is in the same folder.")

    st.markdown("---")

    st.markdown("### 💬 Submit Your Feedback or Upload Your Resume for Review")

    with st.form(key="resume_feedback_form_tab2"):
        reviewer_name = st.text_input("Your Name (Optional)")
        user_role = st.selectbox("I am a...", ["Job Seeker", "Recruiter", "Other"])
        rating = st.slider("How would you rate our sample resumes?", 1, 5, value=5)
        comment = st.text_area("Leave a comment")
        submit_feedback = st.form_submit_button("Submit Feedback")

