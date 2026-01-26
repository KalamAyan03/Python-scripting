import smtplib  # Email bhejne ke liye standard library (Simple Mail Transfer Protocol)
from email.message import EmailMessage  # Modern email format banane ke liye class
import os  # System folders aur environment variables access karne ke liye
from dotenv import load_dotenv  # .env file se secret passwords read karne ke liye
import time  # Script ko sulaane (sleep) aur time dikhane ke liye
import yfinance as yf  # Yahoo Finance se live stock data khichne ke liye
from datetime import datetime  # Aaj ka din aur exact time pata karne ke liye

# 1. Environment variables load karein (.env file mein jo likha hai wo memory mein aa jayega)
load_dotenv()

# --- Logic: Stock price hit hone par email bhejna ---
def logicForEmailSend(netweb, bhel, kaynes):
    # .env se email aur app password nikal kar variables mein daalna (Security purpose)
    __email = os.getenv('EMAIL_USER') 
    __app_password = os.getenv('EMAIL_PASS') 
 
    # Naya email object create karna
    msg = EmailMessage()
    # Email ki main body (message) set karna
    msg.set_content(f"🚨 PORTFOLIO ALERT BHAI! \n\nNetweb: ₹{netweb:.2f}\nBHEL: ₹{bhel:.2f}\nKaynes: ₹{kaynes:.2f}\n\nTarget hit ho gaya hai, check kar lo!")
    msg["Subject"] = "Stock Price Buy Alert!" # Email ka subject
    msg["From"] = __email # Bhejne wale ka email
    msg["To"] = "kalamayan842@gmail.com" # Jisko email jayega

    try:
        # Gmail ke secure server (SSL) se connect karna port 465 par
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(__email, __app_password) # Login process
            server.send_message(msg) # Email ko final send karna
        print("✅ Alert Email bhej diya gaya hai!")
    except Exception as e:
        # Agar internet ya login mein galti ho toh crash na ho, bas error print kare
        print(f"❌ Email bhejne mein galti: {e}")

# --- Logic: Check karna ki market khula hai ya nahi ---
def get_market_status():
    """Check karta hai ki kya market abhi active hai (Monday-Friday aur 9:15-3:30)"""
    now = datetime.now() # Abhi ka exact time aur date
    weekday = now.weekday() # Din pata karna (0 = Monday, 5 = Sat, 6 = Sun)
    
    # Check 1: Sirf Monday (0) se Friday (4) ke beech kaam kare
    if weekday <= 4:
        # Check 2: Indian Market hours (9:15 AM to 3:30 PM) ko decimal mein badalna
        # 9:15 matlab 9.25 ghante aur 15:30 (3:30 PM) matlab 15.5 ghante
        current_time = now.hour + now.minute/60
        if 9.25 <= current_time <= 15.5:
            return True # Market timing ke andar hai
    return False # Market ya toh holiday/weekend hai ya band ho chuka hai

# --- Main Logic: Stocks ko monitor karna ---
def monitor_market():
    # Aapke "Battle Lines" (Jab price inse niche jayega, tabhi alert aayega)
    bhel_target = 233.0
    netweb_target = 2850.0
    kaynes_target = 3100.0

    print("--- 🕵️ Master Market Monitor Started ---")

    while True: # Infinite loop: Script ko Oracle server par 24/7 chalta rakhega
        try:
            # Hum "5d" (5 days) mangwa rahe hain taaki hamesha "Last Available Price" mile
            # Bhale hi aaj Sunday ho, ye pichle working day (Friday) ka data utha lega
            tickers = {"BHEL": "BHEL.NS", "NETWEB": "NETWEB.NS", "KAYNES": "KAYNES.NS"}
            current_prices = {}

            # Har stock ke liye loop chalana
            for name, symbol in tickers.items():
                data = yf.Ticker(symbol).history(period="5d") # 5 din ki history mangwana
                if not data.empty:
                    # Sabse aakhri row (latest price) uthana
                    current_prices[name] = data['Close'].iloc[-1]
                else:
                    current_prices[name] = None # Agar data nahi mila

            # Variables mein prices store karna
            b_now = current_prices["BHEL"]
            n_now = current_prices["NETWEB"]
            k_now = current_prices["KAYNES"]

            # Agar teeno stocks ka price mil gaya hai
            if b_now and n_now and k_now:
                # Terminal par status dikhana: OPEN hai ya CLOSED
                status = "OPEN" if get_market_status() else "CLOSED/WEEKEND"
                print(f"[{time.ctime()}] Market: {status}") # time.ctime() real date-time dikhayega
                print(f"Latest Price -> BHEL: {b_now:.2f} | Netweb: {n_now:.2f} | Kaynes: {k_now:.2f}")

                # --- Alert Logic ---
                # Email alert sirf tabhi jayega jab Market sach mein OPEN ho (Monday-Friday)
                if get_market_status():
                    # Check: Kya koi bhi ek stock target hit kar gaya?
                    if (b_now <= bhel_target or n_now <= netweb_target or k_now <= kaynes_target):
                        print("🚨 TARGET HIT! Email trigger kar raha hoon...")
                        logicForEmailSend(n_now, b_now, k_now)
                        # Alert ke baad 1 ghante (3600s) sula dena taaki spam na ho
                        time.sleep(3600) 
                    else:
                        # Agar target hit nahi hua, toh 15 min (900s) baad dobara check karna
                        print("Prices are high. Waiting 15 mins...")
                        time.sleep(900)
                else:
                    # Agar market band hai (Weekend/Night), toh sirf price dikhao aur 1 ghanta wait karo
                    print("Market band hai, alerts paused. Next check in 1 hour.")
                    time.sleep(3600)

        except Exception as e:
            # Agar internet ud jaye ya Yahoo down ho, toh script crash na ho, 1 min baad retry kare
            print(f"❌ Error: {e}")
            time.sleep(60)

# --- Script Entry Point ---
if __name__ == "__main__":
    # Iske bina code run hona shuru nahi hoga
    monitor_market()