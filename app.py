import os
import re
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='', template_folder='.')
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback-secret-key")

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")

def is_valid_email(email):
    # Simple regex for email validation
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        return False
    # Only allow gmail.com addresses
    domain = email.split('@')[-1].lower()
    return domain == "gmail.com"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    from_email = request.form.get('from')
    user_email = request.form.get('user_email')
    subject = request.form.get('subject')
    body = request.form.get('body')
    attachment = request.files.get('attachment')

    # Validate user email
    if not is_valid_email(user_email):
        flash("Please enter a valid Gmail address (ending with @gmail.com).")
        return redirect('/')

    # Compose the email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = from_email  # Send to yourself
    msg['Reply-To'] = user_email
    msg.set_content(f"Message from: {user_email}\n\n{body}")

    # Handle attachment
    if attachment and attachment.filename:
        file_data = attachment.read()
        if len(file_data) > 15 * 1024 * 1024:
            flash("Attachment exceeds 15MB limit.")
            return redirect('/')
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=attachment.filename)

    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.send_message(msg)
        flash("Your message has been sent!")
    except Exception as e:
        print("Email send error:", e)
        flash("Failed to send email. Please try again later.")

    return redirect('/')

if __name__ == '__main__':
    # For local development only; use gunicorn for production
    app.run(debug=True)

# Gunicorn entry point
# To run with gunicorn: gunicorn --bind 0.0.0.0:8000 app:app
