""" email-csv.py 
write python code to send an email through gmail for each record in a CSV file
"""

import csv
import smtplib  # for sending emails
# for creating the email message:
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Globals:
CSV_FILENAME = 'contacts.csv'


# Gmail account credentials
sender_email = "your_email@gmail.com"  # obtain from .env file or Akeyless.com
sender_password = "your_app_password"  # obtain from .env file or Akeyless.com

# SMTP server configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Read the CSV file and send emails
with open(CSV_FILENAME, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        for row in csv_reader:
            recipient_email = row['email']
            name = row['name']

            # Create the email message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = "Personalized Email"

            # Email body
            body = f"Hello {name},\n\nThis is a personalized email for you."
            message.attach(MIMEText(body, 'plain'))

            # Send the email
            server.send_message(message)
            print(f"Email sent to {recipient_email}")

print(f"*** All emails sent successfully from {CSV_FILENAME}")

