import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from modules import user, ebook, question, feedback, transaction, analytics
from modules.helper import authenticate_user, load_json, save_json
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'zip', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Admin/Employee/User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = authenticate_user(email, password)
        if role:
            session['email'] = email
            session['role'] = role
            return redirect(url_for(f'{role}_dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

# Admin dashboard
@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

# Employee dashboard
@app.route('/employee')
def employee_dashboard():
    if session.get('role') != 'employee':
        return redirect(url_for('login'))
    return render_template('employee_dashboard.html')

# User dashboard
@app.route('/dashboard')
def dashboard():
    if not session.get('email'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# AI Chatbot Interface
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# File Converter
@app.route('/converter', methods=['GET', 'POST'])
def converter():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        format = request.form['format']
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'temp', filename)
            uploaded_file.save(filepath)
            # Convert logic here (mocked)
            flash('File converted successfully.')
    return render_template('converter.html')

# Image to Anime
@app.route('/image-to-anime', methods=['GET', 'POST'])
def image_to_anime():
    return render_template('image_to_anime.html')

# Text to Video
@app.route('/text-to-video', methods=['GET', 'POST'])
def text_to_video():
    return render_template('text_to_video.html')

# Photo to Video
@app.route('/photo-to-video', methods=['GET', 'POST'])
def photo_to_video():
    return render_template('photo_to_video.html')

# Ebook Store
@app.route('/ebook-store')
def ebook_store():
    return render_template('ebook_store.html')

# AI Art Generator
@app.route('/ai-art', methods=['GET', 'POST'])
def ai_art():
    return render_template('ai_art.html')

# Voice Assistant
@app.route('/voice-chat', methods=['GET', 'POST'])
def voice_chat():
    return render_template('voice_chat.html')

# Audiobook Generator
@app.route('/audiobook-dashboard')
def audiobook_dashboard():
    return render_template('audiobook_dashboard.html')

# Leaderboard
@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

# Upgrade Plans
@app.route('/upgrade')
def upgrade():
    return render_template('upgrade.html')

# Wallet Page
@app.route('/wallet')
def wallet():
    return render_template('wallet.html')

# Forum / Your Idea
@app.route('/forum')
def forum():
    return render_template('forum.html')

# Settings / Themes
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')

# Notifications
@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

# Upload Ebook
@app.route('/upload-ebook', methods=['GET', 'POST'])
def upload_ebook():
    return render_template('upload_ebook.html')

# AI Training Mode
@app.route('/ai-training-mode')
def ai_training_mode():
    return render_template('ai_training_mode.html')

# Analytics Dashboard
@app.route('/analytics-dashboard')
def analytics_dashboard():
    return render_template('analytics_dashboard.html')

# Global Search
@app.route('/search')
def search():
    return render_template('search_results.html')

# Maintenance Mode Page
@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')

# 404 Error Custom Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
    