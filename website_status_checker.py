import requests
import time
import smtplib
from email.message import EmailMessage




while True:

    with open("websites.txt", "r") as file:  #opens the file in read mode
        websites = file.readlines() # real all the lines and store in list
        
    websites = [site.strip() for site in websites if site.strip()]   # this will remove the spaces and /n when we add into websites(which is a list) from the .txt file  


    print(websites)


    def sendEmail(statuscode):
        if(response.status_code != 200 ):
                print("--------------------------------------------------")
                print("Status code we recieved is not 200 but it is :", statuscode)
                print("----------------------------------------------------")
                __email = "write your email here"
                __app_password = "write app password of your email it will look like -> "asdf iksd erwe aeew""

                msg = EmailMessage()
                msg.set_content(f"Alert: Website is down. Status code we received is: {statuscode}")
                msg["Subject"] = "Website Alert"
                msg["From"] = "happysingh03030303@gmail.com"
                msg["To"] = "kalamayan842@gmail.com"

                server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  #This connects your script to Gmail’s email server.
                                                                   #465 is Gmail’s secure SMTP port.
                server.login(email, app_password)
                server.send_message(msg)
                server.quit()

  

    for website in websites:
        try :

            response = requests.get(website)
            print("response received from : ", response.url)
            print("status code : ", response.status_code)

            sendEmail(response.status_code)


        except:
            print(f"Unable to connect to server : {website}")

    for n in range(5):
        print(" __ ", end = " ", flush=True) #by default python adds \n at last so we said end with " " and flush it immediately. 
                                                # as if print() does not end with \n then the output is stored in buffer and print when program ends or buffers get full
                                                # so to flush the buffer data immediately we used "flush == True"
        time.sleep(1)
    print("\n")


