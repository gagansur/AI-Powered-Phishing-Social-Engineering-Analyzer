import streamlit as st
import google.generativeai as genai
import os

# 1. Setup API Key with fallback
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# 2. DEBUG SECTION: This identifies what models YOUR key can actually see
try:
    models = [m.name for m in genai.list_models()]
    st. sidebar.write("✅ API Connected")
    st. sidebar.write(f"Available Models: {models}")
    
    # Logic to auto-select the best available model
    if 'models/gemini-1.5-flash' in models:
        target_model = 'gemini-1.5-flash'
    elif 'models/gemini-pro' in models:
        target_model = 'gemini-pro'
    else:
        target_model = models[0] if models else "gemini-pro."
        
except Exception as e:
    st. sidebar.error(f"❌ API Error: {e}")
    target_model = "gemini-pro"

# 3. Initialize Model
model = genai.GenerativeModel('gemini-2.5-flash')
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
