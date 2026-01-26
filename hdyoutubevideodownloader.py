from yt_dlp import YoutubeDL

video_url = input("Enter YouTube video URL: ")

ydl_options = {

    # yeh line ensure karti hai ki:
    # best video stream + best audio stream download ho
    # aur agar possible ho to dono merge ho jaayein
    "format": "bestvideo+bestaudio/best",

    # yeh ensure karta hai ki final output mp4 me aaye
    "merge_output_format": "mp4",

    # file ka naam video ke title ke according ho
    "outtmpl": "%(title)s.%(ext)s"
}

with YoutubeDL(ydl_options) as ydl:
    ydl.download([video_url])
