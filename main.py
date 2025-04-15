import tkinter as tk
from gtts import gTTS
from playsound import playsound
from transformers import pipeline
from tkinter import messagebox, scrolledtext
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import re
import threading

def clear_status(delay=3000):
    root.after(delay, lambda: status_label.config(text=""))

def is_bangla(text):
    # Check if the text contains Bangla characters
    for char in text:
        if '\u0980' <= char <= '\u09FF':
            return True
    return False

def get_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([^&\n]+)", url)
    return match.group(1) if match else None

def fetch_transcript():
    url = entry.get().strip()
    video_id = get_video_id(url)
    
    if not video_id:
        messagebox.showerror("Error", "Invalid YouTube URL")
        return

    try:
        # Try to get transcript in preferred languages
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try Bangla or English
        transcript = None
        for lang_code in ['bn', 'en']:
            try:
                transcript = transcript_list.find_transcript([lang_code])
                break
            except NoTranscriptFound:
                continue

        if not transcript:
            messagebox.showinfo("Transcript", "No transcript found in Bangla or English.")
            return

        fetched_transcript = transcript.fetch()
        transcript_text = "\n".join([getattr(entry, 'text', str(entry)) if hasattr(entry, 'text') else entry['text'] for entry in fetched_transcript])

        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, transcript_text)

    except VideoUnavailable:
        messagebox.showerror("Error", "This video is unavailable.")
    except TranscriptsDisabled:
        messagebox.showerror("Error", "Transcripts are disabled for this video.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

def summarize_transcript():
    full_text = text_area.get("1.0", tk.END).strip()
    if not full_text:
        messagebox.showinfo("No Text", "Please fetch a transcript first.")
        return

    status_label.config(text="Detecting language and summarizing...")

    def summarize_task():
        try:
            is_bn = is_bangla(full_text)

            model_name = "csebuetnlp/mT5_multilingual_XLSum"
            local_summarizer = pipeline("summarization", model=model_name, tokenizer=model_name)

            chunk_size = 800
            chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]

            summary = ""
            for chunk in chunks:
                result = local_summarizer(chunk, max_length=100, min_length=20, do_sample=False)
                summary += result[0]['summary_text'].strip() + "\n\n"

            def update_ui():
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, summary.strip())
                status_label.config(text="Summarization complete!")
                clear_status()

            root.after(0, update_ui)

        except Exception as e:
            print("Error:", e)
            root.after(0, lambda: messagebox.showerror("Error", f"Summarization failed:\n{str(e)}"))
            root.after(0, lambda: status_label.config(text=""))

    threading.Thread(target=summarize_task).start()

def speak_summary():
    text = text_area.get("1.0", tk.END).strip()
    if not text:
        messagebox.showinfo("No Text", "Please summarize the transcript first.")
        return
    
    # Use gTTS to generate speech from the summarized text
    lang_code = 'bn' if is_bangla(text) else 'en'  # Select language based on detected content
    try:
        tts = gTTS(text, lang=lang_code)
        tts.save("summary.mp3")  # Save the speech as an MP3 file
        playsound("summary.mp3")  # Play the saved MP3 file
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while speaking the text:\n{str(e)}")

# GUI Setup
root = tk.Tk()
root.title("YouTube Transcript Fetcher")

tk.Label(root, text="Enter YouTube Video URL:").pack(pady=5)
entry = tk.Entry(root, width=60)
entry.pack(pady=5)
status_label = tk.Label(root, text="", fg="blue")
status_label.pack(pady=5)

tk.Button(root, text="Get Transcript", command=fetch_transcript).pack(pady=5)
tk.Button(root, text="Summarize Transcript", command=summarize_transcript).pack(pady=5)
tk.Button(root, text="🔊 Speak Summary", command=speak_summary).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25)
text_area.pack(padx=10, pady=10)

root.mainloop()
