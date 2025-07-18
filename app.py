import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from modules import user, ebook, question, feedback, transaction, analytics
from modules.helper import authenticate_user, load_json, save_json
from dotenv import load_dotenv
from flask import Flask, render_template, request, session
from flask_session import Session
from modules.chatbot_logic import get_answer_from_json, get_fallback_ai_response
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'zip', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# -------------------- Auth & Login --------------------
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -------------------- Dashboards --------------------
@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/employee')
def employee_dashboard():
    if session.get('role') != 'employee':
        return redirect(url_for('login'))
    return render_template('employee_dashboard.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('email'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# -------------------- Main Features --------------------

@app.route('/converter', methods=['GET', 'POST'])
def converter():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        format = request.form['output_format']
        if uploaded_file and format:
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'temp', filename)
            uploaded_file.save(filepath)
            flash('File converted successfully.')
    return render_template('converter.html')

@app.route('/admin/manage-qa', methods=['GET', 'POST'])
def manage_qa():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    qa_data = load_json('data/qa_data.json')
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        role = request.form['role']
        new_qa = {'question': question, 'answer': answer}
        if role not in qa_data:
            qa_data[role] = []
        qa_data[role].append(new_qa)
        save_json('data/qa_data.json', qa_data)
        flash('Q&A Added Successfully.')
    return render_template('admin_add_qa.html', qa_data=qa_data)

@app.route('/image-to-anime', methods=['GET', 'POST'])
def image_to_anime():
    return render_template('image_to_anime.html')

@app.route('/text-to-video', methods=['GET', 'POST'])
def text_to_video():
    return render_template('text_to_video.html')

@app.route('/photo-to-video', methods=['GET', 'POST'])
def photo_to_video():
    return render_template('photo_to_video.html')

@app.route('/ebook-store')
def ebook_store():
    return render_template('ebook_store.html')

@app.route('/ai-art', methods=['GET', 'POST'])
def ai_art():
    image_url = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        # You can integrate real Stable Diffusion here later
        image_url = f"/static/images/placeholder.jpg"
    return render_template('ai_art.html', image_url=image_url)

@app.route('/voice-chat', methods=['GET', 'POST'])
def voice_chat():
    return render_template('voice_chat.html')

@app.route('/audiobook-dashboard')
def audiobook_dashboard():
    return render_template('audiobook_dashboard.html')

def update_leaderboard(user_data):
    leaderboard = load_json('data/leaderboard.json')
    for key in ['country', 'state', 'city']:
        entry = next((e for e in leaderboard[key] if e['name'] == user_data[key]), None)
        if entry:
            entry['count'] += 1
        else:
            leaderboard[key].append({'name': user_data[key], 'count': 1})
    save_json('data/leaderboard.json', leaderboard)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'chat_history' not in session:
        session['chat_history'] = []
    role = session.get('role', 'guest')
    if request.method == 'POST':
        user_input = request.form['user_input']
        answer = get_answer_from_json(user_input, role) or get_fallback_ai_response(user_input)
        session['chat_history'].append({'role': 'user', 'text': user_input})
        session['chat_history'].append({'role': 'bot', 'text': answer})
        if 'user_data' in session:
            update_leaderboard(session['user_data'])
    return render_template('chatbot.html', chat_history=session['chat_history'])

@app.route('/upgrade')
def upgrade():
    return render_template('upgrade.html')

@app.route('/wallet')
def wallet():
    return render_template('wallet.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        language = request.form['language']
        session['language'] = language
        flash('Language preference saved.')
    return render_template('settings.html')

@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    if session.get('role') not in ['admin', 'employee']:
        return redirect(url_for('login'))
    notifications = load_json('data/notifications.json')
    if request.method == 'POST':
        audience = request.form['audience']
        message = request.form['message']
        new_note = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "audience": audience,
            "message": message
        }
        notifications.append(new_note)
        save_json('data/notifications.json', notifications)
        flash('Notification sent!')
    return render_template('notifications.html', notifications=notifications)

@app.route('/upload-ebook', methods=['GET', 'POST'])
def upload_ebook():
    return render_template('upload_ebook.html')

@app.route('/ai-training-mode')
def ai_training_mode():
    return render_template('ai_training_mode.html')

@app.route('/analytics-dashboard')
def analytics_dashboard():
    return render_template('analytics_dashboard.html')

@app.route('/search')
def search():
    return render_template('search_results.html')

@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')

# -------------------- Actions & Logic --------------------
@app.route('/send-notification', methods=['POST'])
def send_notification():
    if session.get('role') not in ['admin', 'employee']:
        return redirect(url_for('login'))
    audience = request.form['audience']
    message = request.form['message']
    flash('Notification sent successfully!')
    return redirect(url_for('notifications'))

@app.route('/subscribe', methods=['POST'])
def subscribe_plan():
    plan_id = request.form['plan_id']
    flash('Plan subscription successful!')
    return redirect(url_for('upgrade'))

# -------------------- Error Handler --------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404

# -------------------- Run --------------------
if __name__ == '__main__':
    app.run(debug=True)
