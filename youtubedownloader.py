from yt_dlp import YoutubeDL

video_url = input("enter youtube link : ") # enter url here

ydl_options =   {
                    "format" : "best",
                    "outtmpl": "%(title)s.%(ext)s"
                }

with YoutubeDL(ydl_options) as ydl:
    ydl.download([video_url])