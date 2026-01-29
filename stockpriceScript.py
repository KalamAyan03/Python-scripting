# ================= REQUIRED MODULES IMPORT =================

import smtplib
# smtplib = Python ki standard library jo email bhejne ke kaam aati hai
# Ye SMTP (Simple Mail Transfer Protocol) ka use karti hai

from email.message import EmailMessage
# EmailMessage = modern aur structured tareeka email ka content banane ke liye

import os
# os module = system environment variables (.env) se data read karne ke liye

from dotenv import load_dotenv
# load_dotenv = .env file ke secrets ko program ki memory mein load karta hai

import time
# time module = delay dene ke liye (sleep), taaki script bar-bar spam na kare

import yfinance as yf
# yfinance = Yahoo Finance se stock prices (live / recent) nikalne ke liye

from datetime import datetime
# datetime = current date aur time nikalne ke liye

import logging
# logging = print() ka professional replacement (file + terminal logging)

# ================= LOGGING SETUP =================

logging.basicConfig(
    level=logging.INFO,
    # level INFO ka matlab: INFO, WARNING, ERROR sab log honge

    format="%(asctime)s - %(levelname)s - %(message)s",
    # format batata hai ki har log line ka structure kaisa hoga

    handlers=[
        logging.FileHandler("stock_market_price_monitor.log"),
        # FileHandler = saare logs is file mein save honge

        logging.StreamHandler()
        # StreamHandler = same logs terminal par bhi dikhayega
    ]
)

# =================================================

load_dotenv()
# .env file load ho rahi hai taaki EMAIL aur PASSWORD mil sake

# ================= EMAIL ALERT LOGIC =================

def logicForEmailSend(netweb, bhel, kaynes):
    # Ye function tab call hota hai jab koi stock apna target hit karta hai

    __email = os.getenv('EMAIL_USER')
    # EMAIL_USER environment variable se sender email read kar raha hai

    __app_password = os.getenv('EMAIL_PASS')
    # EMAIL_PASS (Gmail App Password) ko secure tareeke se read kar raha hai

    msg = EmailMessage()
    # Email ka naya object create ho raha hai

    msg.set_content(
        f"🚨 PORTFOLIO ALERT BHAI!\n\n"
        f"Netweb: ₹{netweb:.2f}\n"
        f"BHEL: ₹{bhel:.2f}\n"
        f"Kaynes: ₹{kaynes:.2f}\n\n"
        f"Target hit ho gaya hai, check kar lo!"
    )
    # Email ka main message body set ho raha hai

    msg["Subject"] = "Stock Price Buy Alert!"
    # Email ka subject

    msg["From"] = __email
    # Sender ka email address

    msg["To"] = "kalamayan842@gmail.com"
    # Receiver ka email address

    try:
        # Gmail ke SMTP server ke saath secure SSL connection ban raha hai

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(__email, __app_password)
            # Gmail account login ho raha hai

            server.send_message(msg)
            # Email send ho raha hai

        logging.info("Alert email successfully bhej diya gaya hai")
        # Email successfully bhejne ka log

    except Exception as e:
        logging.error(f"Email bhejne mein error aayi: {e}")
        # Agar email fail ho jaaye toh error log

# ================= MARKET STATUS CHECKER =================

def get_market_status():
    # Ye function check karta hai market abhi open hai ya nahi

    now = datetime.now()
    # Current date aur time nikal raha hai

    weekday = now.weekday()
    # Weekday number (0 = Monday, 6 = Sunday)

    if weekday <= 4:
        # Sirf Monday se Friday tak allow

        current_time = now.hour + now.minute / 60
        # Time ko decimal format mein convert kar raha hai

        if 9.25 <= current_time <= 15.5:
            # Indian stock market timing: 9:15 AM to 3:30 PM
            return True

    return False
    # Weekend ya market band hone par False

# ================= MAIN MARKET MONITOR =================

def monitor_market():
    # Ye function poori script ka main engine hai

    bhel_target = 233.0
    netweb_target = 2850.0
    kaynes_target = 3100.0
    # Ye buy targets define kar rahe hain

    logging.info("🕵️ Master Market Monitor started")
    # Script start hone ka log

    while True:
        # Infinite loop = script continuously chalegi

        try:
            tickers = {
                "BHEL": "BHEL.NS",
                "NETWEB": "NETWEB.NS",
                "KAYNES": "KAYNES.NS"
            }
            # Stock names aur unke Yahoo Finance symbols

            current_prices = {}
            # Latest prices store karne ke liye dictionary

            for name, symbol in tickers.items():
                data = yf.Ticker(symbol).history(period="5d")
                # Last 5 trading days ka data fetch kar raha hai

                if not data.empty:
                    current_prices[name] = data["Close"].iloc[-1]
                    # Latest closing price store kar raha hai
                else:
                    current_prices[name] = None
                    logging.warning(f"{name} ka data empty mila")
                    # Agar Yahoo se data na mile toh warning

            b_now = current_prices["BHEL"]
            n_now = current_prices["NETWEB"]
            k_now = current_prices["KAYNES"]
            # Prices ko variables mein assign kar rahe hain

            if b_now and n_now and k_now:
                status = "OPEN" if get_market_status() else "CLOSED / WEEKEND"
                # Market status decide kar raha hai

                logging.info(f"Market Status: {status}")

                logging.info(
                    f"Latest Prices | BHEL: {b_now:.2f} | "
                    f"Netweb: {n_now:.2f} | Kaynes: {k_now:.2f}"
                )
                # Latest prices log kar raha hai

                if get_market_status():
                    # Market open hone par hi email alert allow

                    if (b_now <= bhel_target or
                        n_now <= netweb_target or
                        k_now <= kaynes_target):

                        logging.warning("🚨 TARGET HIT! Email trigger ho raha hai")
                        logicForEmailSend(n_now, b_now, k_now)

                        time.sleep(3600)
                        # Alert ke baad 1 ghanta sleep (spam avoid)

                    else:
                        logging.info("Prices abhi target ke upar hain, 15 min wait")
                        time.sleep(900)

                else:
                    logging.info("Market band hai, alerts paused. Next check in 1 hour")
                    time.sleep(3600)
            break #remove this to run script in loop
            

        except KeyboardInterrupt:
            # Jab user Ctrl + C dabata hai, yahan execution aata hai

            logging.info("🛑 Script manually closed by user (Ctrl + C)")
            # Clean shutdown ka log

            break
            # Infinite loop se bahar nikal ke script ko safely band karta hai

        except Exception as e:
            # Koi bhi unexpected error aaye toh script crash na ho

            logging.error(f"Unexpected error aayi: {e}")
            time.sleep(60)
            # 1 minute wait karke dobara try kare
            break #remove this to run script in loop

# ================= SCRIPT ENTRY POINT =================

if __name__ == "__main__":
    # Ye ensure karta hai ki script sirf direct run hone par start ho
    monitor_market()
