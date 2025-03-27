from flask import Flask, request, send_file
import base64
import os

app = Flask(__name__)
PDF_PATH = "output.pdf"

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json()
    if not data or "base64" not in data:
        return {"error": "No base64 data provided"}, 400

    try:
        pdf_data = base64.b64decode(data["base64"])
        with open(PDF_PATH, "wb") as f:
            f.write(pdf_data)
        return {"message": "PDF saved successfully"}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/download", methods=["GET"])
def download():
    if not os.path.exists(PDF_PATH):
        return {"error": "PDF not found"}, 404
    return send_file(PDF_PATH, mimetype='application/pdf', as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
