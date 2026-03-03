import streamlit as st
import google.generativeai as genai
import os

# 1. Setup Page Config
st.set_page_config(page_title="AI Phishing Scout", page_icon="🛡️")
st.title("🛡️ AI Phishing & Social Engineering Scout")
st.write("Paste any suspicious email below to see the AI's risk analysis.")

# 2. Secure API Key (For Streamlit Cloud)
# In your local test, you can use os.getenv. In the cloud, we'll use st. secrets.
api_key = st.secrets["GOOGLE_API_KEY"] if "GOOGLE_API_KEY" in st.secrets else os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. User Interface
email_input = st.text_area("Paste Email Content Here:", height=250, placeholder="Example: Dear user, your account is locked...")

if st.button("Analyze Email"):
    if email_input:
        with st.spinner('Analyzing tactics...'):
            prompt = f"""
            Act as a Senior Cyber Security Analyst. Analyze this email for phishing:
            {email_input}
            Return a report with: 
            - Risk Level (Safe/Low/Medium/High)
            - Detected Tactics (e.g., sense of urgency, fake authority)
            - Final Verdict
            """
            response = model.generate_content(prompt)
            st.subheader("Analysis Result:")
            st.info(response.text)
    else:
        st.warning("Please paste an email first!")
