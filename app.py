from flask import Flask, request, jsonify
from cerebras.cloud.sdk import Cerebras
import os

app = Flask(__name__)

# This pulls the API Key from Render's Environment Variables
client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        user_prompt = data.get("prompt", "")

        # System Prompt: This tells the AI HOW to answer.
        # We want RAW JSON so Roblox can read it easily.
        response = client.chat.completions.create(
            model="llama3.1-8b", 
            messages=[
                {
                    "role": "system", 
                    "content": "You are a Roblox building bot. Output ONLY a JSON array of parts. "
                               "Each part must have: 'Name', 'Size' (Vector3 as list [x,y,z]), "
                               "'Position' (Vector3 as list [x,y,z]), and 'Color' (string). "
                               "No conversation, no markdown blocks, just the raw array."
                },
                {"role": "user", "content": user_prompt}
            ]
        )
        
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
