from flask import Blueprint, request, jsonify
import requests

prompt_generator_bp = Blueprint('prompt_generator', __name__, url_prefix='/prompt_generator')

API_URL_TESTING = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HEADERS_TESTING = {"Authorization": "Bearer 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"}

API_URL = "https://ctagpxdbl3lg09zh.us-east-1.aws.endpoints.huggingface.cloud"
HEADERS = {
	"Accept" : "application/json",
	"Authorization": "Bearer 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",
	"Content-Type": "application/json" 
}

def queryTesting(payload):
    response = requests.post(API_URL_TESTING, headers=HEADERS_TESTING, json=payload)
    return response.json()

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

sys_prompt = f"""
You are a well-structured system prompt generator for Large Language models.
Your task is to convert yhe given vague prompt into a well-structured system prompt.
"""

@prompt_generator_bp.route('/generate/test', methods=['POST'])
def summarizeTesting():
    if request.method == 'POST':
        try:
            data = request.json
            input_text = data.get('input_text')
            if input_text:
                output = queryTesting({"inputs": input_text})
                return jsonify(output), 200
            else:
                return jsonify({'error': 'Input text is required.'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

@prompt_generator_bp.route('/generate', methods=['POST'])
def summarize():
    if request.method == 'POST':
        try:
            data = request.json
            input_text = data.get('input_text')
            if input_text:
                input = f"<s>[INST]<<SYS>>{sys_prompt}<</SYS>{input_text}[/INST]"
                output = query({
	                            "inputs": input,
	                            "parameters": {
		                            "max_new_tokens": 150
	                            }
                            })
                return jsonify(output), 200
            else:
                return jsonify({'error': 'Input text is required.'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500