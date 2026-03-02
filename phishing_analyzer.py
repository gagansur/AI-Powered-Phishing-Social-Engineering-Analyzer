import google.generativeai as genai

# 1. Setup your API Key
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_email(email_content):
    # 2. The "Security Prompt" (This is the secret sauce for your resume)
    prompt = f"""
    Act as a Senior Cyber Security Analyst. Analyze the following email for signs of phishing, 
    social engineering, or malicious intent. 
    
    Provide a report in this format:
    - Risk Score: (0-10)
    - Tactics Detected: (e.g., Urgency, Authority, Suspicious Link)
    - Analysis: (Why it is or isn't suspicious)
    
    Email Content:
    ---
    {email_content}
    ---
    """
    
    response = model.generate_content(prompt)
    return response.text

# 3. Test it
sample_email = "URGENT: Your account has been locked. Click here to verify: http://bit.ly/fake-link"
print(analyze_email(sample_email))
