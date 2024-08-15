from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Replace with your actual Gemini API details
GEMINI_API_KEY = 'AIzaSyCtbYipWNUH5tqwFs67cmdprDggOMme9sk'
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
genai.configure(api_key=GEMINI_API_KEY)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
