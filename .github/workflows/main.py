import os
import smtplib
from email.message import EmailMessage
import time
import requests

def fetch_university_updates():
    simulated_announcement = """
    Department of Computer Science - 4th Year AI: 
    New Directed Work (TD) on Stochastic Processes and Markov Chains has been posted. 
    Submission deadline is next Thursday.
    """
    return simulated_announcement

def process_with_gemini(raw_text):
    api_key = os.environ["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"You are a precise academic assistant for a 4th-year AI Engineering student. Extract exact deadlines, module names, exam topics, and action items clearly in both English and Arabic without fluff.\n\nUpdate: {raw_text}"
            }]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    # Automatically retry up to 3 times if a 503 high demand spike occurs
    for attempt in range(3):
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        elif response.status_code == 503 and attempt < 2:
            print(f"Server overloaded (503), retrying attempt {attempt + 2} in 5 seconds...")
            time.sleep(5)
        else:
            raise Exception(f"Gemini API Error {response.status_code}: {response.text}")

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
    
    print("Processing content with Gemini API via HTTP...")
    ai_summary = process_with_gemini(raw_content)
    print(ai_summary)
    
    print("Sending email alert...")
    send_gmail_notification(ai_summary)
