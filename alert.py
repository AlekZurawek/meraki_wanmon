import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define email addresses and login credentials
sender_email = "your source email goes here"
receiver_email = "your destination email goes here"
password = "your soruce email password goes here"

# Define function to send email alert
def send_email(serial, interface, status1, status2):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = f"{serial} {interface} {status1} changed to {status2}"
    body = f"{serial} {interface} {status1} has changed to {status2}"
    message.attach(MIMEText(body, 'plain'))
    text = message.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

# Read log file and store last status for each serial on each interface
last_status = {}
with open("log.txt", "r") as file:
    for line in file:
        line = line.strip().split()
        serial, interface, status = line[2], line[3], line[4]
        last_status[(serial, interface)] = status

# Continuously check for changes in log file
while True:
    with open("log.txt", "r") as file:
        for line in file:
            line = line.strip().split()
            serial, interface, status = line[2], line[3], line[4]
            if (serial, interface) in last_status and last_status[(serial, interface)] != status:
                send_email(serial, interface, last_status[(serial, interface)], status)
                last_status[(serial, interface)] = status
    time.sleep(110) # Wait for 10 seconds before checking again