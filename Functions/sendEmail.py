from Functions.mylibraries import *

def send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, app_password):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Create the server connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection

    # Login to the email server
    server.login(sender_email, app_password)

    # Send the email
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)

    # Quit the server connection
    server.quit()

# Example usage
send_email(
    sender_email="rachid.chentouf71@gmail.com",
    receiver_email="rachid.axiom@gmail.com",
    subject='Buy/Sell Alert',
    body='This is a test email sent from Python!',
    smtp_server='smtp.gmail.com',
    smtp_port=587,
    app_password='foicfxiwfxwirtjb'
)