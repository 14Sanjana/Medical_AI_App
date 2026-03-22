from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from chatbot import chatbot_response   # Your AI function

app = Flask(__name__)
app.secret_key = "super_secret_key"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# =========================
# 1️⃣ Landing Page
# =========================
@app.route('/')
def landing():
    return render_template('landing.html')


# =========================
# 2️⃣ Login Page
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            session['user'] = username
            return redirect(url_for('select'))
        else:
            return "Invalid login credentials"

    return render_template('login.html')


# =========================
# 3️⃣ Select Page
# =========================
@app.route('/select')
def select():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('select.html')


# =========================
# 4️⃣ Upload Skin
# =========================
@app.route('/upload/skin', methods=['GET', 'POST'])
def upload_skin():
    if request.method == 'POST':
        file = request.files.get('image')

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Reset chat when new result comes
            session.pop("chat_history", None)

            # Temporary hardcoded result
            session['result'] = "Skin Cancer Detected"
            session['confidence'] = 87
            session['severity'] = "High"
            session['disease_type'] = "skin"

            return redirect(url_for('chatbot'))

    return render_template('upload_skin.html')


# =========================
# 5️⃣ Upload X-Ray
# =========================
@app.route('/upload/xray', methods=['GET', 'POST'])
def upload_xray():
    if request.method == 'POST':
        file = request.files.get('image')

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Reset chat when new result comes
            session.pop("chat_history", None)

            # Temporary hardcoded result
            session['result'] = "Pneumonia Detected"
            session['confidence'] = 92
            session['severity'] = "Moderate"
            session['disease_type'] = "xray"

            return redirect(url_for('chatbot'))

    return render_template('upload_xray.html')


# =========================
# 6️⃣ Chatbot Page
# =========================
@app.route('/chatbot')
def chatbot():
    if 'result' not in session:
        return redirect(url_for('select'))

    if 'chat_history' not in session:
        session['chat_history'] = []

    return render_template(
        'chatbot.html',
        result=session.get('result'),
        confidence=session.get('confidence'),
        severity=session.get('severity'),
        chat_history=session.get('chat_history')
    )


# =========================
# 7️⃣ Handle Chatbot Message
# =========================
@app.route('/chatbot-response', methods=['POST'])
def handle_chatbot_response():
    user_question = request.form.get('user_question')

    if not user_question:
        return redirect(url_for('chatbot'))

    reply = chatbot_response(user_question)

    if 'chat_history' not in session:
        session['chat_history'] = []

    chat_history = session['chat_history']
    chat_history.append({"role": "user", "message": user_question})
    chat_history.append({"role": "bot", "message": reply})

    session['chat_history'] = chat_history

    return redirect(url_for('chatbot'))


# =========================
# 8️⃣ Clear Chat (FIXED)
# =========================
@app.route("/clear_chat")
def clear_chat():
    session.pop("chat_history", None)
    return redirect(url_for("chatbot"))   # ✅ Correct redirect


# =========================
# Run App
# =========================
if __name__ == '__main__':
    app.run(debug=True)
