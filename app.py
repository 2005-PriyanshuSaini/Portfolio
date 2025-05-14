import os
import re
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, flash, session, abort
from functools import wraps
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

def csrf_protect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            token = session.get('_csrf_token')
            form_token = request.form.get('_csrf_token')
            if not token or not form_token or token != form_token:
                abort(400, description="CSRF token missing or invalid.")
        return f(*args, **kwargs)
    return decorated_function

def generate_csrf_token():
    import secrets
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_urlsafe(32)
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

@app.after_request
def set_secure_headers(response):
    # Prevent aggressive caching of HTML so new deploys are always loaded
    if request.path == "/" or request.path.endswith(".html"):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline' fonts.googleapis.com cdnjs.cloudflare.com; font-src 'self' fonts.gstatic.com cdnjs.cloudflare.com; script-src 'self' 'unsafe-inline' cdnjs.cloudflare.com; img-src 'self' data:;"
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
@csrf_protect
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
