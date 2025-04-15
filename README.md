# 🎬 YouTube Video Summarizer

A Python GUI application that fetches, summarizes, and reads out transcripts from YouTube videos in **English** and **Bangla**. Built using `Tkinter`, `Transformers`, and `gTTS`, this tool helps you save time by providing quick summaries of video content.

---

## ✨ Features

- 🔍 Fetch YouTube video transcripts (supports both Bangla & English)
- ✂️ Summarize long transcripts using state-of-the-art NLP
- 🎧 Listen to summaries via text-to-speech
- 🖼️ Simple GUI built with Tkinter
- 🌐 Supports both `youtu.be` and full `youtube.com` URLs

---



## 📦 Requirements

Before running this app, make sure you have the following installed:


gTTS==2.3.2
playsound==1.2.2
transformers==4.39.3
torch>=1.13.0
youtube-transcript-api==0.6.1

To install all at once:
```
pip install -r requirements.txt
```

## How to run:
1. Clone this repository
   ```
   git clone https://github.com/Mahidul-Ratul/Youtube-Video-Summarizer.git
   cd Youtube-Video-Summarizer
   ```
2.Install the dependencies:
   ```
     pip install -r requirements.txt
   ```
3.Run the app:
   ```
     python youtube_summarizer.py
   ```

## Languages Supported:
 1.Bangla (bn)

 2.English (en)


## Model Info
Summarization is powered by:

csebuetnlp/mT5_multilingual_XLSum
A multilingual summarization model from HuggingFace

#License
This project is licensed under the MIT License. Feel free to modify and use it!











