from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "API çalışıyor"})


@app.route("/translate", methods=["POST"])
def translate():
    data = request.json

    if not data or "text" not in data:
        return jsonify({
            "error": "text zorunlu"
        }), 400

    text = data.get("text")
    target_language = data.get("target_language", "English")  # default

    try:
        prompt = f"""
Detect the source language of the following text and translate it into {target_language}.

Return the result strictly in JSON format like this:
{{
  "detected_language": "...",
  "translated_text": "..."
}}

Text:
{text}
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        # AI çıktısı JSON string olacak
        result = response.output_text

        return jsonify(eval(result))  # controlled output

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
