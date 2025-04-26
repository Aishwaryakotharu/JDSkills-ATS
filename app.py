import streamlit as st
import json
from datetime import datetime
from PIL import Image

# Page configuration with horizontal tabs
st.set_page_config(page_title="PM JD Skill | Skills Extractor", page_icon="🧠", layout="wide")

# Define tabs (horizontal)
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
        feedback_text = st.text_area("✍️ Leave your comment or resume feedback request here:", key="comment_input_tab2")
        uploaded_resume = st.file_uploader("📎 Upload your resume (PDF or DOCX)", type=["pdf", "docx"], key="upload_input_tab2")
        rating = st.slider("⭐ How would you rate our sample resumes?", 1, 5, 4, key="rating_slider_tab2")

        submitted = st.form_submit_button("Submit Feedback", use_container_width=True)

        if submitted:
            st.success("✅ Thank you! Your feedback has been received.")

            if feedback_text:
                st.markdown(f"**Your Comment:** {feedback_text}")
            st.markdown(f"**Your Rating:** {rating} ⭐")

            if uploaded_resume:
                st.markdown(f"**Uploaded Resume:** `{uploaded_resume.name}`")

                # Save feedback and resume to the JSON file
                data = {
                    "comment": feedback_text,
                    "rating": rating,
                    "file_name": uploaded_resume.name,
                    "timestamp": str(datetime.now())
                }
                
                # Load existing feedback or initialize an empty list
                try:
                    with open('feedback_data.json', 'r') as f:
                        feedback_data = json.load(f)
                except FileNotFoundError:
                    feedback_data = []

                # Add new feedback to the list
                feedback_data.append(data)

                # Save updated feedback list back to JSON
                with open('feedback_data.json', 'w') as f:
                    json.dump(feedback_data, f)

# ---------------- Tab 3: Feedback & Discussion Board ----------------
with tab3:
    st.title("💬 Feedback & Discussion Board")

    # Load all feedback from JSON file
    try:
        with open('feedback_data.json', 'r') as f:
            feedback_data = json.load(f)
    except FileNotFoundError:
        feedback_data = []

    if feedback_data:
        for feedback in feedback_data:
            st.subheader(f"📝 Comment from {feedback['timestamp']}")
            st.markdown(f"**Feedback:** {feedback['comment']}")
            st.markdown(f"**Rating:** {feedback['rating']} ⭐")
            st.markdown(f"**Resume Submitted:** `{feedback['file_name']}`")
            st.markdown("---")

            # Like functionality
            if st.button("👍 Like", key=feedback['timestamp']):
                st.success("You liked this submission!")

            # Comment on the feedback
            comment = st.text_area("💬 Add a comment or feedback:", key=f"comment_{feedback['timestamp']}")
            if st.button("💬 Submit Comment", key=f"submit_comment_{feedback['timestamp']}"):
                st.success(f"Your comment: `{comment}` has been submitted!")

    else:
        st.warning("No feedback or resumes have been submitted yet.")
