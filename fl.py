import requests
from flask import Flask, Response, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("main.html")


@app.route("/video")
def video():
    return render_template("index5.html")


@app.route("/get_video", methods=["POST"])
def get_video():
    text = request.json.get("text")
    # text = "hello"
    print(text)

    # Assuming your API endpoint is at http://127.0.0.1:8000/video
    api_url = "http://127.0.0.1:8000/video"

    # Make a POST request to your API
    response = requests.post(api_url, json={"text": text}, stream=True)

    # Forward the response from the API to the client
    return Response(
        response.iter_content(chunk_size=1024),
        content_type="video/mp4",
    )


if __name__ == "__main__":
    app.run(debug=True)
