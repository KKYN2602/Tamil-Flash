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
    accuracy = fuzz.ratio(spoken_text, expected_text)
    if accuracy > 90:
        return jsonify({"message": f"✅ Perfect pronunciation! ({accuracy}%)"})
    elif accuracy > 50:
        return jsonify({"message": f"⚠️ Almost correct! ({accuracy}%) Try again."})
    else:
        return jsonify({"message": f"❌ Incorrect pronunciation. ({accuracy}%) Try again."})

@app.route("/next_card")
def next_card():
    global current_card
    if not to_learn:
        return jsonify({"error": "No more words to learn!"})
    current_card = random.choice(to_learn)
    return jsonify(current_card)

@app.route('/flashcard')
def flashcard():
    if not to_learn:
        return render_template('flash_card.html', card={"Tamil": "No more words!", " English": ""})
    card = random.choice(to_learn)
    return render_template('flash_card.html', card=card)

@app.route("/mark_known", methods=["POST"])
def mark_known():
    global to_learn
    if current_card in to_learn:
        to_learn.remove(current_card)
        pd.DataFrame(to_learn).to_csv("data/words_to_learn.csv", index=False)
    return jsonify({"message": "Word marked as known!"})

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        today = datetime.utcnow().date()
        last_login = user.last_login.date()
        if last_login == today:
            pass
        elif last_login == today - timedelta(days=1):
            user.streak += 1
        else:
            user.streak = 1
        user.last_login = datetime.utcnow()
        db.session.commit()
        session["user_id"] = user.id
        return redirect(url_for('index'))
    return "Invalid credentials. Please try again."

@app.route('/signup', methods=['POST'])
def do_signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return "Username or email already exists. Please choose a different one."
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = User.query.get(session["user_id"])
    return render_template("dashboard.html", user=user)

@app.route('/alphabets')
def alphabets():
    alphabet_data = load_data("alphabets.json")
    return render_template('alphabets.html', vowels=alphabet_data["vowels"], data=alphabet_data["consonants"])

@app.route('/family')
def family():
    data = load_data('family.json')
    return render_template('family.html', data=data)

@app.route('/numbers')
def numbers():
    data = load_data('numbers.json')
    return render_template('numbers.html', data=data)

@app.route('/times_day')
def times_day():
    data = load_data('times_day.json')
    return render_template('times_day.html', time=data['time'], days=data['days_of_week'])

@app.route('/colors')
def colors():
    data = load_data('colors.json')
    return render_template('colors.html', colors=data['colors'])

@app.route('/common_phrases')
def common_phrases():
    data = load_data('common_phrases.json')
    return render_template('common_phrases.html', common_phrases=data)

@app.route('/map', endpoint='map')
def tamil_cultural_map():
    return render_template('map.html')

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        db.session.delete(user)
        db.session.commit()
        session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route('/update_account', methods=['POST'])
def update_account():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = User.query.get(session["user_id"])
    username = request.form.get('username')
    email = request.form.get('email')
    user.username = username
    user.email = email
    db.session.commit()
    return redirect(url_for('account'))

@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.streak.desc()).all()
    return render_template('leaderboard.html', users=users)

translator = Translator()

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        text_to_translate = request.form['text']
        translated = translator.translate(text_to_translate, src='en', dest='ta')
        return render_template('translate.html', translated_text=translated.text)
    return render_template('translate.html')

@app.route('/voice_assistant')
def voice_assistant():
    return render_template('voice_assistant.html')

@app.route('/kural-of-the-day')
def kural_of_the_day():
    kural = get_kural_of_the_day()
    return render_template('kural_of_the_day.html', kural=kural)

@app.route('/account')
def account():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = User.query.get(session["user_id"])
    user.progress = getattr(user, 'progress', 50)
    user.xp = getattr(user, 'xp', 100)
    user.badges = getattr(user, 'badges', [])
    user.activities = getattr(user, 'activities', [])
    user.join_date = getattr(user, 'join_date', datetime.utcnow())
    user.profile_image_url = getattr(user, 'profile_image_url', None)
    return render_template('account.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/get_tamil_response', methods=['POST'])
def get_tamil_response():
    data = request.get_json()
    user_input = data.get('text', '')
    translated = translator.translate(user_input, src='en', dest='ta')
    return jsonify({"response": translated.text})

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        selected_questions = session.get('selected_questions')
        if not selected_questions:
            return redirect(url_for('quiz'))
        score = 0
        for i, question in enumerate(selected_questions):
            user_answer = request.form.get(f'q{i}')
            if user_answer == question['answer']:
                score += 1
        return render_template('quiz_result.html', score=score, total=len(selected_questions))
    with open('data/quiz_questions.json', 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    selected_questions = random.sample(all_questions, 10)
    session['selected_questions'] = selected_questions
    return render_template('quiz.html', questions=selected_questions)

def reset_streaks():
    today = datetime.utcnow().date()
    users = User.query.all()
    for user in users:
        if user.last_login.date() < today - timedelta(days=1):
            user.streak = 0
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
