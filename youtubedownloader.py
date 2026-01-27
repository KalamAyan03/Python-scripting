# yahan hum yt_dlp library ke andar se YoutubeDL class ko import kar rahe hain
# yt_dlp ek powerful library hai jo YouTube se video download karna jaanti hai
# YoutubeDL ek class hai (class = blueprint) jo downloader ka behaviour define karti hai
from yt_dlp import YoutubeDL


# yahan hum user se YouTube video ka link input le rahe hain
# input() function program ko rok deta hai aur user se value maangta hai
# jo bhi link user paste karega, wo video_url variable me store ho jayega
video_url = input("Enter YouTube video URL: ")


# yahan hum downloader ke liye options define kar rahe hain
# yeh ek dictionary hai (dictionary = key-value pair structure)
# is dictionary ke through hum yt-dlp ko batate hain ki kaise download karna hai
ydl_options = {

    # "format": "best" ka matlab hai ki sabse best available quality ka video download karo
    # agar highest resolution available hogi to wahi select hogi
    "format": "bestvideo+bestaudio/best",
    # "format":"best" # this will download decent video quality

    # "outtmpl" ka matlab hai output file ka naam kaise banega
    # %(title)s ka matlab hai video ka title use karo
    # %(ext)s ka matlab hai correct file extension use karo jaise .mp4 ya .webm
    "outtmpl": "%(title)s.%(ext)s"
}


# yahan hum 'with' statement ka use kar rahe hain
# with ka use resource ko safely handle karne ke liye hota hai
# resource yahan YoutubeDL object hai jo network connection aur files use karta hai
# with ensure karta hai ki kaam khatam hone ke baad sab kuch automatically clean ho jaye
with YoutubeDL(ydl_options) as ydl:

    # yeh line actual download start karti hai
    # ydl.download() function YouTube page ko analyze karta hai
    # phir best video aur audio streams ko download karta hai
    # aur last me unhe merge karke ek final file bana deta hai
    # [video_url] list me isliye diya gaya hai kyunki yt-dlp multiple URLs bhi accept karta hai
    ydl.download([video_url])


# jaise hi with block khatam hota hai, Python automatically:
# network connections close kar deta hai
# temporary files remove kar deta hai
# memory free kar deta hai
# yeh sab kaam hume manually nahi karna padta, isi liye with bahut important hai
