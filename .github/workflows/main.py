import os
import smtplib
from email.message import EmailMessage
from google import genai

# 1. Initialize Gemini Client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def fetch_university_updates():
    # TODO: Add your university scraping/requests logic here (e.g., scraping Moodle or departmental portal)
    # For now, this simulates finding a new lecture or announcement text:
    simulated_announcement = """
    Department of Computer Science - 4th Year AI: 
    New Directed Work (TD) on Stochastic Processes and Markov Chains has been posted. 
    Submission deadline is next Thursday.
    """
    return simulated_announcement

def process_with_gemini(raw_text):
    prompt = f"""
    Analyze this university update. Provide a clear, concise summary and extract any deadlines or action items in both Arabic and English:
    {raw_text}
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

def send_gmail_notification(summary_text):
    sender_email = os.environ["GMAIL_USER"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    
    msg = EmailMessage()
    msg.set_content(summary_text)
    msg['Subject'] = '🎓 Smart Academic Update: New University Notice'
    msg['From'] = sender_email
    msg['To'] = sender_email  # Sends the alert to your own Gmail

    # Connect to Gmail SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)
    print("Email notification sent successfully to Gmail!")

if __name__ == "__main__":
    print("Checking university platform...")
    raw_content = fetch_university_updates()
    
    print("Processing content with Gemini AI...")
    ai_summary = process_with_gemini(raw_content)
    print(ai_summary)
    
    print("Sending email alert...")
    send_gmail_notification(ai_summary)
