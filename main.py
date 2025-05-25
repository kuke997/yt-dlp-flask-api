from flask import Flask, request, jsonify
import yt_dlp
import tempfile
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "yes"

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing 'url'"}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "quiet": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            return jsonify({
                "title": info.get("title"),
                "filename": os.path.basename(filename),
                "status": "success"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)