from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import login_required, current_user
from flask_bootstrap import Bootstrap
import json
import pandas as pd
import random
from googletrans import Translator
import os
from rapidfuzz import fuzz
import base64
import cv2
import numpy as np
import pytesseract
from models import db, User
from datetime import datetime, timedelta
from kurals import get_kural_of_the_day

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/tamil_words.csv")

to_learn = data.to_dict(orient="records")
current_card = {}

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tamilflash.db'
db.init_app(app)
Bootstrap(app)

with app.app_context():
    db.create_all()

def load_data(filename):
    with open(f"data/{filename}", encoding='utf-8') as f:
        return json.load(f)

def save_data(filename, data):
    with open(f"data/{filename}", 'w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/writing_pad")
def writing_pad():
    return render_template("writing_pad.html")

@app.route("/detect_word", methods=["POST"])
def detect_word():
    try:
        data = request.get_json()
        image_data = data["image"].split(",")[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((2, 2), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        text = pytesseract.image_to_string(dilated, lang="tam")
        cleaned_text = text.strip()
        return jsonify({"word": cleaned_text if cleaned_text else "No text detected."})
    except Exception as e:
        print("Error during OCR:", e)
        return jsonify({"word": "❌ Error processing image."}), 500

@app.route("/pronunciation")
def pronunciation():
    kural = {
        "number": 1,
        "line1": "அகர முதல எழுத்தெல்லாம் ஆதி",
        "line2": "பகவன் முதற்றே உலகு",
        "meaning": "As the letter A is the first of all letters, so is the Almighty the first in the world."
    }
    all_words = (kural["line1"] + " " + kural["line2"]).split()
    word_to_pronounce = random.choice(all_words)
    session['correct_word'] = word_to_pronounce
    return render_template("pronunciation.html", word=word_to_pronounce)

@app.route("/check_pronunciation", methods=["POST"])
def check_pronunciation():
    data = request.get_json()
    spoken_text = data.get("spoken", "").strip()
    expected_text = data.get("expected")
    if not spoken_text:
        return jsonify({"message": "⚠️ Didn't catch that. Please speak clearly."})
    if expected_text:
        expected_text = expected_text.strip()
    else:
        expected_text = session.get('correct_word', '').strip()
    accuracy = fuzz.ratio(spoken_text, e_
