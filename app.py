import os
from flask import Flask, render_template, request, send_file
import requests
import io
import base64

app = Flask(__name__)

# Replace with your actual API key
API_KEY = os.getenv("API_KEY")
API_HOST = 'https://api.stability.ai'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        try:
            response = requests.post(
                f"{API_HOST}/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                },
                json={
                    "text_prompts": [
                        {
                            "text": prompt
                        }
                    ],
                    "cfg_scale": 7,
                    "height": 1024,
                    "width": 1024,
                    "samples": 1,
                    "steps": 30,
                },
            )

            if response.status_code != 200:
                raise Exception("Non-200 response: " + str(response.text))

            data = response.json()
            image_base64 = data["artifacts"][0]["base64"]
            image_data = base64.b64decode(image_base64)

            return render_template('index.html', image=base64.b64encode(image_data).decode('utf-8'), prompt=prompt)
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)