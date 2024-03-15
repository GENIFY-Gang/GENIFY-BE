from flask import Blueprint, request, jsonify
import requests

prompt_generator_bp = Blueprint('prompt_generator', __name__, url_prefix='/prompt_generator')

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HEADERS = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

@prompt_generator_bp.route('/generate', methods=['POST'])
def summarize():
    if request.method == 'POST':
        try:
            data = request.json
            input_text = data.get('input_text')
            if input_text:
                output = query({"inputs": input_text})
                return jsonify(output), 200
            else:
                return jsonify({'error': 'Input text is required.'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500