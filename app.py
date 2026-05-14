from flask import Flask, request, jsonify
from flask_cors import CORS

from services.youtube_service import (
    get_youtube_qualities,
    download_youtube_video
)

from services.instagram_service import (
    get_instagram_video
)

app = Flask(__name__)
CORS(app)


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "message": "Video Downloader API"
    })


# =========================
# YOUTUBE QUALITIES
# =========================
@app.route("/youtube/qualities", methods=["POST"])
def youtube_qualities():

    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({
            "success": False,
            "message": "URL missing"
        }), 400

    try:
        qualities = get_youtube_qualities(url)
        if not qualities:

            return jsonify({
                "success": False,
                "error": "No formats found"
                }), 500

        return jsonify({
            "success": True,
            "qualities": qualities
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================
# YOUTUBE DOWNLOAD
# =========================
@app.route("/youtube/download", methods=["POST"])
def youtube_download():

    data = request.get_json()

    url = data.get("url")
    format_id = data.get("format_id")

    if not url or not format_id:
        return jsonify({
            "success": False,
            "message": "Missing data"
        }), 400

    try:
        result = download_youtube_video(url, format_id)

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================
# INSTAGRAM DOWNLOAD
# =========================
@app.route("/instagram/download", methods=["POST"])
def instagram_download():

    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({
            "success": False,
            "message": "URL missing"
        }), 400

    try:
        result = get_instagram_video(url)

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )