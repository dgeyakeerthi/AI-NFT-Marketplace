from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from generate_image import generate_image
import uuid
import os

app = Flask(__name__)
CORS(app)

# Home route
@app.route("/")
def home():
    return "AI NFT Backend Running"


# Generate Image Route
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Generate image using Stability API
        image_bytes = generate_image(prompt)

        # Create folder if not exists
        os.makedirs("generated", exist_ok=True)

        # Unique filename
        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join("generated", filename)

        # Save image
        with open(filepath, "wb") as f:
            f.write(image_bytes)

        # Return JSON response
        return jsonify({
            "message": "Image generated successfully",
            "image_path": f"generated/{filename}",
            "image_url": f"http://127.0.0.1:5000/generated/{filename}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Serve generated images
@app.route("/generated/<filename>")
def get_image(filename):
    return send_from_directory("generated", filename)

if __name__ == "__main__":
    app.run(debug=True)