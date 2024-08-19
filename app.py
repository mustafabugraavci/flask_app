# app.py

from flask import Flask, render_template, request
import json
import requests
import google.generativeai as genai

app = Flask(__name__)

# Replace with your actual Gemini API details

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate():
    response = model.generate_content("Describe how this product might be manufactured.")
    print(response.text)


if __name__ == '__main__':
    app.run(debug=True)
