from flask import Flask, render_template, request
import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

response = requests.get("https://api.npoint.io/674f5423f73deab1e9a7")
response.raise_for_status()
blog_articles = response.json()

smtp_server = 'smtp.gmail.com'
smtp_port = 587
receiver_email = os.getenv("RECIPIENT")
gmail_address = os.getenv("GMAIL_ADDRESS")
gmail_password = os.getenv("GMAIL_PASSWORD")

@app.route('/')
def home():
    return render_template("index.html", blog=blog_articles)

@app.route('/posts/<int:id>')
def posts(id):
    return render_template("post.html", blog=blog_articles, id=id)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=['POST','GET'])
def contact():
    method = request.method
    if method == "GET":
        return render_template("contact.html", method=method)
    else:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        # Create the email
        subject = 'New Entry'
        body = f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}'

        # Set up the MIME structure
        email_message = MIMEMultipart()
        email_message['From'] = gmail_address
        email_message['To'] = receiver_email
        email_message['Subject'] = subject
        email_message.attach(MIMEText(body, 'plain'))
        try:
            # Establish a connection to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Upgrade the connection to secure encrypted mode
            server.login(gmail_address, gmail_password)  # Use app password
            server.sendmail(gmail_address, receiver_email, email_message.as_string())
            print("Email has been successfully sent.")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            server.quit()
        return render_template("contact.html", method=method)


if __name__ == "__main__":
    app.run(debug=True)