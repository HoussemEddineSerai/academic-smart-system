import os
import smtplib
from email.message import EmailMessage
from google import genai
from google.genai import types

# 1. Initialize Gemini Client using environment variables
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def fetch_university_updates():
    # TODO: Add your university scraping/requests logic here (e.g., Moodle or departmental portal)
    # Simulated announcement for testing pipeline:
    simulated_announcement = """
    Department of Computer Science - 4th Year AI: 
    New Directed Work (TD) on Stochastic Processes and Markov Chains has been posted. 
    Submission deadline is next Thursday.
    """
    return simulated_announcement

def process_with_gemini(raw_text):
    # Using the modern Gemini 3.8 Flash model with explicit system instructions
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        config=types.GenerateContentConfig(
            system_instruction="You are a precise academic assistant for a 4th-year AI Engineering student. Extract exact deadlines, module names, exam topics, and action items clearly in both English and Arabic without fluff.",
            temperature=0.3,
        ),
        contents=raw_text
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

    try:
        # Connect to Gmail SMTP server securely
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        print("Email notification sent successfully to Gmail!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e

if __name__ == "__main__":
    print("Checking university platform...")
    raw_content = fetch_university_updates()
    
    print("Processing content with Gemini AI...")
    ai_summary = process_with_gemini(raw_content)
    print(ai_summary)
    
    print("Sending email alert...")
    send_gmail_notification(ai_summary)
