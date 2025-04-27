import streamlit as st
import pandas as pd
import random
from streamlit_modal import Modal

# Mock data
jobs = [
    {"id": 1, "title": "Web Developer Needed", "description": "Looking for an experienced web developer to build a responsive website.", "engagement": "Full-time", "experiencelevel": "Intermediate", "skills": "HTML, CSS, JavaScript, React"},
    {"id": 2, "title": "Python Data Analyst", "description": "Seeking a data analyst proficient in Python to analyze large datasets.", "engagement": "Part-time", "experiencelevel": "Expert", "skills": "Python, Pandas, NumPy, Data Visualization"},
    {"id": 3, "title": "Mobile App Developer", "description": "Need a skilled mobile app developer for iOS and Android platforms.", "engagement": "Contract", "experiencelevel": "Intermediate", "skills": "Swift, Kotlin, React Native"},
    {"id": 4, "title": "UI/UX Designer", "description": "Looking for a creative UI/UX designer to improve our product's user experience.", "engagement": "Full-time", "experiencelevel": "Expert", "skills": "Figma, Adobe XD, Sketch, User Research"},
    {"id": 5, "title": "DevOps Engineer", "description": "Seeking a DevOps engineer to streamline our deployment processes.", "engagement": "Full-time", "experiencelevel": "Expert", "skills": "Docker, Kubernetes, AWS, CI/CD"},
]

proposal_settings = {
    1: {"id": 1, "user_id": 1, "prompt": "Write a professional Upwork proposal for the following job. The proposal should be concise, highlight relevant skills, and show enthusiasm for the project."}
}

# Functions
def fetch_job_listings(filters=None, sort_by=None, sort_order=None):
    df = pd.DataFrame(jobs)
    if filters:
        for key, value in filters.items():
            if value:
                df = df[df[key].str.contains(value, case=False)]
    
    if sort_by and sort_order:
        df = df.sort_values(by=sort_by, ascending=(sort_order == "ascending"))
    
    return df

def get_or_create_proposal_settings(user_id):
    if user_id in proposal_settings:
        return proposal_settings[user_id]
    else:
        new_settings = {"id": len(proposal_settings) + 1, "user_id": user_id, "prompt": "Write a professional Upwork proposal for the following job. The proposal should be concise, highlight relevant skills, and show enthusiasm for the project."}
        proposal_settings[user_id] = new_settings
        return new_settings

def generate_proposal(job, settings):
    intro = f"Dear Client,\n\nI am excited to apply for the {job['title']} position. With my expertise in {job['skills']}, I am confident that I can deliver excellent results for your project."
    
    body = f"Your project requires {job['experiencelevel']} level skills, and I have extensive experience in {', '.join(job['skills'].split(', ')[:2])}. I have successfully completed several {job['engagement']} projects similar to yours."
    
    approach = "My approach would be to:"
    for i in range(3):
        approach += f"\n{i+1}. {random.choice(['Analyze your requirements in detail', 'Develop a comprehensive plan', 'Implement best practices', 'Ensure regular communication', 'Deliver high-quality work'])}"
    
    closing = f"\nI'm excited about the opportunity to work on this project and would love to discuss it further. Please feel free to reach out if you have any questions or would like to schedule a call.\n\nBest regards,\n[Your Name]"
    
    return f"{intro}\n\n{body}\n\n{approach}\n\n{closing}"

# Streamlit app
st.title("Upwork Proposal Writer")

# Sidebar for navigation
page = st.sidebar.radio("Navigation", ["Job Listings", "Settings"])

if page == "Job Listings":
    st.header("Job Listings")

    # Filters and Sorting
    st.subheader("Filters and Sorting")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        title_filter = st.text_input("Title")
    with col2:
        engagement_filter = st.selectbox("Engagement", ["", "Full-time", "Part-time", "Contract"])
    with col3:
        experience_filter = st.selectbox("Experience Level", ["", "Entry", "Intermediate", "Expert"])
    with col4:
        sort_by = st.selectbox("Sort by", ["", "title", "engagement", "experiencelevel"])
    with col5:
        sort_order = st.selectbox("Sort order", ["ascending", "descending"])

    filters = {
        "title": title_filter,
        "engagement": engagement_filter,
        "experiencelevel": experience_filter
    }

    job_listings = fetch_job_listings(filters, sort_by, sort_order)

    # Create a modal for job details
    modal = Modal("Job Details", key="job_details_modal")

    # Display job listings in a table with action buttons
    for _, job in job_listings.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 2, 0.5, 0.5])
        with col1:
            st.write(job['title'])
        with col2:
            st.write(job['engagement'])
        with col3:
            st.write(job['experiencelevel'])
        with col4:
            st.write(job['skills'])
        with col5:
            if st.button("👁️", key=f"view_{job['id']}"):
                modal.open()
                if modal.is_open():
                    with modal.container():
                        st.subheader(f"Job Details: {job['title']}")
                        st.write(f"**Description:** {job['description']}")
                        st.write(f"**Engagement:** {job['engagement']}")
                        st.write(f"**Experience Level:** {job['experiencelevel']}")
                        st.write(f"**Skills:** {job['skills']}")
        with col6:
            if st.button("📝", key=f"generate_{job['id']}"):
                user_id = 1  # Mock user ID
                settings = get_or_create_proposal_settings(user_id)
                
                with st.spinner("Generating proposal..."):
                    proposal = generate_proposal(job, settings)
                
                st.subheader(f"Generated Proposal for {job['title']}")
                st.text_area("Proposal", proposal, height=400, key=f"proposal_{job['id']}")
        
        st.write("---")

elif page == "Settings":
    st.header("Proposal Settings")
    user_id = 1  # Mock user ID
    settings = get_or_create_proposal_settings(user_id)
    
    new_prompt = st.text_area("Customize your proposal prompt:", value=settings["prompt"], height=200)
    if st.button("Save Settings"):
        settings["prompt"] = new_prompt
        st.success("Settings saved successfully!")

# Add some CSS to improve the app's appearance
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .stSelectbox {
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)