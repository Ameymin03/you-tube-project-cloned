# # # from fastapi import FastAPI, HTTPException
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from youtube_transcript_api import YouTubeTranscriptApi
# # # from urllib.parse import urlparse, parse_qs
 
# # # app = FastAPI()
 
# # # # Enable CORS for all origins (for frontend use)
# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )
 
# # # def extract_video_id(url: str):
 
# # #     try:
# # #         parsed_url = urlparse(url)
# # #         hostname = parsed_url.hostname
# # #         if hostname in ['www.youtube.com', 'youtube.com']:
# # #             if parsed_url.path == '/watch':
# # #                 # Standard: https://www.youtube.com/watch?v=VIDEO_ID
# # #                 query_params = parse_qs(parsed_url.query)
# # #                 return query_params.get('v', [None])[0]
# # #             elif parsed_url.path.startswith('/embed/'):
# # #                 # Embed: https://www.youtube.com/embed/VIDEO_ID
# # #                 return parsed_url.path.split('/embed/')[1]
# # #         elif hostname == 'youtu.be':
# # #             # Short: https://youtu.be/VIDEO_ID
# # #             return parsed_url.path.lstrip('/')
# # #         return None
# # #     except Exception:
# # #         return None
 
# # # @app.get("/")
# # # async def root():
# # #     return {"message": "YouTube Transcript API is running."}
 
# # # @app.get("/process")
# # # async def process_video(video_url: str):
# # #     video_id = extract_video_id(video_url)
# # #     if not video_id:
# # #         raise HTTPException(status_code=400, detail="Invalid or unsupported YouTube URL format.")
 
# # #     try:
# # #         transcript = YouTubeTranscriptApi.get_transcript(video_id)
# # #         text = " ".join([item['text'] for item in transcript])
# # #         return {"transcript": text}
# # #     except Exception as e:
# # #         raise HTTPException(status_code=400, detail=f"Could not fetch transcript: {str(e)}")
 
# # # # --- Script functionality: Print transcript if run directly ---
# # # if __name__ == "__main__":
# # #     video_id = "P6FORpg0KVo"  # The ID from your YouTube link
# # #     print(f"Transcript for video ID: {video_id}\n")
# # #     try:
# # #         transcript = YouTubeTranscriptApi.get_transcript(video_id)
# # #         for entry in transcript:
# # #             print(entry['text'])
# # #     except Exception as e:
# # #         print(f"Error fetching transcript: {e}")

# # # backend/main.py
# # from fastapi import FastAPI, HTTPException
# # from fastapi.middleware.cors import CORSMiddleware
# # from youtube_transcript_api import YouTubeTranscriptApi
# # from urllib.parse import urlparse, parse_qs

# # app = FastAPI()

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # def extract_video_id(url: str):
# #     parsed_url = urlparse(url)
# #     if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
# #         if parsed_url.path == '/watch':
# #             query_params = parse_qs(parsed_url.query)
# #             return query_params.get('v', [None])[0]
# #         elif parsed_url.path.startswith('/embed/'):
# #             return parsed_url.path.split('/embed/')[1]
# #     elif parsed_url.hostname == 'youtu.be':
# #         return parsed_url.path.lstrip('/')
# #     return None

# # def summarize_text(text: str) -> str:
# #     # Simple summary: first 3 sentences (replace with a real model if you want)
# #     import re
# #     sentences = re.split(r'(?<=[.!?]) +', text)
# #     summary = ' '.join(sentences[:3])
# #     return summary if summary else text[:200] + "..."

# # @app.get("/")
# # async def root():
# #     return {"message": "YouTube Transcript API is running."}

# # @app.get("/process")
# # async def process_video(video_url: str):
# #     video_id = extract_video_id(video_url)
# #     if not video_id:
# #         raise HTTPException(status_code=400, detail="Invalid or unsupported YouTube URL format.")

# #     try:
# #         transcript = YouTubeTranscriptApi.get_transcript(video_id)
# #         text = " ".join([item['text'] for item in transcript])
# #         summary = summarize_text(text)
# #         return {
# #             "transcript": text,
# #             "summary": summary
# #         }
# #     except Exception as e:
# #         raise HTTPException(status_code=400, detail=f"Could not fetch transcript: {str(e)}")

# fastapi_app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

transcript_store = {}

def extract_video_id(url: str):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed_url.path == '/watch':
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/embed/')[1]
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path.lstrip('/')
    return None

def summarize_text(text: str) -> str:
    sentences = re.split(r'(?<=[.!?]) +', text)
    summary = ' '.join(sentences[:3])
    return summary if summary else text[:200] + "..."

@app.get("/")
async def root():
    return {"message": "YouTube Transcript API is running."}

@app.get("/process")
async def process_video(video_url: str):
    video_id = extract_video_id(video_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid or unsupported YouTube URL format.")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([item['text'] for item in transcript])
        summary = summarize_text(text)
        data = {
            "video_id": video_id,
            "video_url": video_url,
            "transcript": text,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }
        transcript_store[video_id] = data
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch transcript: {str(e)}")

@app.get("/all_transcripts")
async def get_all_transcripts(): 
    return list(transcript_store.values())


# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from youtube_transcript_api import YouTubeTranscriptApi
# from urllib.parse import urlparse, parse_qs
# from datetime import datetime
# from collections import Counter
# import re

# app = FastAPI()

# # Allow frontend (React) to connect
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, specify your frontend URL
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # In-memory store for transcripts (keyed by video_id)
# transcript_store = {}

# def extract_video_id(url: str):
#     """Extract YouTube video ID from a URL."""
#     parsed_url = urlparse(url)
#     if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
#         if parsed_url.path == '/watch':
#             query_params = parse_qs(parsed_url.query)
#             return query_params.get('v', [None])[0]
#         elif parsed_url.path.startswith('/embed/'):
#             return parsed_url.path.split('/embed/')[1]
#     elif parsed_url.hostname == 'youtu.be':
#         return parsed_url.path.lstrip('/')
#     return None

# def summarize_text(text: str, num_sentences: int = 3) -> str:
#     """Summarize the text by extracting the most informative sentences."""
#     # Split text into sentences
#     sentences = re.split(r'(?<=[.!?]) +', text)
#     if len(sentences) <= num_sentences:
#         return text

#     # Tokenize and normalize words
#     words = re.findall(r'\w+', text.lower())
#     word_freq = Counter(words)

#     # Score each sentence based on word frequency
#     sentence_scores = {}
#     for sentence in sentences:
#         word_list = re.findall(r'\w+', sentence.lower())
#         sentence_scores[sentence] = sum(word_freq[word] for word in word_list)

#     # Select top scored sentences
#     top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
#     summary = ' '.join(top_sentences)
#     return summary

# @app.get("/")
# async def root():
#     return {"message": "YouTube Transcript API is running."}

# @app.get("/process")
# async def process_video(video_url: str):
#     video_id = extract_video_id(video_url)
#     if not video_id:
#         raise HTTPException(status_code=400, detail="Invalid or unsupported YouTube URL format.")

#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         text = " ".join([item['text'] for item in transcript])
#         summary = summarize_text(text)
#         data = {
#             "video_id": video_id,
#             "video_url": video_url,
#             "transcript": text,
#             "summary": summary,
#             "timestamp": datetime.now().isoformat()
#         }
#         transcript_store[video_id] = data
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Could not fetch transcript: {str(e)}")

# @app.get("/all_transcripts")
# async def get_all_transcripts(): 
#     """Return all stored transcripts."""
#     return list(transcript_store.values())
