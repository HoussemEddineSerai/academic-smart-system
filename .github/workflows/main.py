import os
import smtplib
from email.message import EmailMessage
from google import genai
from google.genai import types
from google.genai.errors import ServerError

# 1. Initialize Gemini Client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def fetch_university_updates():
    simulated_announcement = """
    Department of Computer Science - 4th Year AI: 
    New Directed Work (TD) on Stochastic Processes and Markov Chains has been posted. 
    Submission deadline is next Thursday.
    """
    return simulated_announcement

def process_with_gemini(raw_text):
    # Tries gemini-3.8-flash first; automatically falls back if 503 high demand happens
    models_to_try = ['gemini-3.8-flash', 'gemini-3.8-flash-lite', 'gemini-3.8-pro']
    
    config = types.GenerateContentConfig(
        system_instruction="You are a precise academic assistant for a 4th-year AI Engineering student. Extract exact deadlines, module names, exam topics, and action items clearly in both English and Arabic without fluff.",
        temperature=0.3,
    )

    last_error = None
    for model_name in models_to_try:
        try:
            print(f"Trying model: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                config=config,
                contents=raw_text
            )
            return response.text
        except ServerError as e:
            print(f"{model_name} overloaded (503), switching to next model...")
            last_error = e

    raise last_error

def send_gmail_notification(summary_text):
    sender_email = os.environ["GMAIL_USER"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    
    msg = EmailMessage()
    msg.set_content(summary_text)
    msg['Subject'] = '🎓 Smart Academic Update: New University Notice'
    msg['From'] = sender_email
    msg['To'] = sender_email

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
