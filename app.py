import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# Set the path for the feedback CSV file
feedback_path = "user_feedback.csv"

# ---------------- Tab 1: JD Skill + ATS Extractor ----------------
with st.expander("📝 JD Skill Extractor"):
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
with st.expander("📄 Resume Samples"):
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

        if submit_feedback:
            feedback_df = pd.DataFrame([{
                "Name": reviewer_name,
                "Role": user_role,
                "Rating": rating,
                "Comment": comment
            }])

            # If feedback file exists, append; otherwise, create a new one
            if os.path.exists(feedback_path):
                existing_df = pd.read_csv(feedback_path)
                feedback_df = pd.concat([existing_df, feedback_df], ignore_index=True)

            feedback_df.to_csv(feedback_path, index=False)
            st.success("✅ Thank you for your feedback!")


# ---------------- Tab 3: Feedback & Discussion Board ----------------
with st.expander("💬 Feedback & Discussion Board"):
    st.title("💬 Feedback & Discussion Board")

    st.subheader("💬 What Users Are Saying")

    # Load feedback data from the CSV file if it exists
    if os.path.exists(feedback_path):
        reviews_df = pd.read_csv(feedback_path)
        # Show last 5 reviews
        for _, row in reviews_df.tail(5).iterrows():
            st.markdown(f"**A {row['Role'].lower()} says:**")
            st.markdown(f"“{row['Comment']}”")
            st.markdown(f"⭐ {row['Rating']}/5")
            st.markdown("---")
    else:
        st.info("No reviews yet — be the first to share feedback!")
