from flask import Flask, request, jsonify
from flask_cors import CORS
from app.engine.answer_engine import generate_answer
from app.utils.image_utils import extract_text_from_base64_image

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "OPTIONS"])
def home():
    return "TDS Virtual TA is running."


@app.route("/api/", methods=["POST"])
def answer_api():
    data = request.get_json()
    question = data.get("question", "").strip()
    image_data = data.get("image")

    if not question and not image_data:
        return jsonify({"error": "Missing 'question' and/or 'image' field."}), 400

    if image_data:
        ocr_text = extract_text_from_base64_image(image_data)
        question += "\n\n[Image OCR Text]\n" + ocr_text

    try:
        result = generate_answer(question)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")
