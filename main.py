# main.py
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

FASTAPI_URL = "http://localhost:8000"  # FastAPI must be running on this port

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = summary = error = ""
    if request.method == "POST":
        video_url = request.form.get("video_url")
        try:
            response = requests.get(f"{FASTAPI_URL}/process", params={"video_url": video_url})
            if response.status_code == 200:
                data = response.json()
                transcript = data.get("transcript", "")
                summary = data.get("summary", "")
            else:
                error = response.json().get("detail", "An error occurred.")
        except Exception as e:
            error = str(e)
    return render_template("index.html", transcript=transcript, summary=summary, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
