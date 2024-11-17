from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Hugging Face Endpoint
HF_ENDPOINT = "https://b3xeyjvju03lme3x.us-east-1.aws.endpoints.huggingface.cloud"
API_KEY = "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"  # Add your Hugging Face API key here

# Default generation parameters
BASE_PARAMS = {
    'do_sample': True,
    'top_k': 50,
    'top_p': 0.95,
    'temperature': 0.8,
    'repetition_penalty': 1.1,
    'no_repeat_ngram_size': 4,
    'num_beams': 2,
    'early_stopping': True,
    'length_penalty': 1.2,
    'bad_words_ids': None,
    'min_length': 10,
    'use_cache': True,
}

@app.route("/")
def health_check():
    """Health check endpoint to verify the API is running."""
    return jsonify({"status": "Healthy", "message": "Flask backend is live!"})


@app.route("/generate", methods=["POST"])
def generate():
    """
    Endpoint to interact with the Hugging Face model.
    Expects a JSON payload with 'input_text' and optional 'params'.
    """
    try:
        # Get input from request
        data = request.get_json()
        input_text = data.get("input_text", "").strip()
        custom_params = data.get("params", {})

        if not input_text:
            return jsonify({"error": "Input text cannot be empty."}), 400

        # Merge default and custom parameters
        generation_params = {**BASE_PARAMS, **custom_params, "inputs": input_text}

        # Make a request to the Hugging Face endpoint
        response = requests.post(
            HF_ENDPOINT,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json=generation_params,
        )
        
        # Handle Hugging Face response
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get("generated_text", "")
            return jsonify({"input": input_text, "output": generated_text})
        else:
            return jsonify({"error": "Error from Hugging Face API", "details": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Run the Flask app locally
    app.run(host="0.0.0.0", port=8080)
