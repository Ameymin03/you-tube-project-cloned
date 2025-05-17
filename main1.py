from flask import Flask, render_template, request
import requests

app = Flask(__name__)

FASTAPI_URL = "https://your-fastapi-url.onrender.com"
  # Make sure FastAPI is running here

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    error = ""

    if request.method == "POST":
        video_url = request.form.get("video_url")

        try:
            response = requests.get(f"{FASTAPI_URL}/process", params={"video_url": video_url})

            if response.status_code == 200:
                data = response.json()
                transcript = data.get("transcript", "").strip()

                # If transcript is empty or missing
                if not transcript:
                    error = "Transcript not available."
            else:
                # FastAPI responded with an error
                error = response.json().get("detail", "An error occurred while processing the video.")
        except Exception as e:
            error = f"Request failed: {str(e)}"

    return render_template("index.html", transcript=transcript, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
