import requests
import time
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()

def sendEmail(statuscode):
    if statuscode != 200:
        print("--------------------------------------------------")
        print("Status code we received is not 200, it is:", statuscode)
        print("--------------------------------------------------")

        __email = os.getenv('EMAIL_USER')
        __app_password = os.getenv('EMAIL_PASS')

        msg = EmailMessage()
        msg.set_content(f"Alert: Website is down. Status code received: {statuscode}")
        msg["Subject"] = "Website Alert"
        msg["From"] = __email
        msg["To"] = "kalamayan842@gmail.com"

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(__email, __app_password)
        server.send_message(msg)
        server.quit()

while True:
    with open("websites.txt", "r") as file:
        websites = [site.strip() for site in file if site.strip()]

    for website in websites:
        try:
            response = requests.get(website, timeout=10)
            print("Response received from:", response.url)
            print("Status code:", response.status_code)

            sendEmail(response.status_code)

        except requests.exceptions.RequestException as e:
            print(f"Unable to connect to server: {website}")
            print("Error:", e)

    for n in range(5):
        print(" __ ", end=" ", flush=True)
        time.sleep(1)

    print("\n")
