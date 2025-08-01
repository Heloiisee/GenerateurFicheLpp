from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from pathlib import Path
from functools import wraps
from weasyprint import HTML
from io import BytesIO
from dotenv import load_dotenv
import glob
import threading
import time
import csv
import os
import uuid 
from PIL import Image

load_dotenv()  # Charge les variables d'environnement depuis .env si présent

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Configuration du dossier de téléchargement
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def clean_temp_files():
    temp_files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], "preview_*"))
    for file_path in temp_files:
        try:
            os.remove(file_path)
            print(f"🗑️ Supprimé au démarrage : {file_path}")
        except Exception as e:
            print(f"⚠️ Erreur suppression : {file_path} -> {e}")

def delete_file_later(filepath, delay=300):
    def delete():
        time.sleep(delay)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"🕔 Supprimé après délai : {filepath}")
            except Exception as e:
                print(f"⚠️ Erreur suppression différée : {e}")
    threading.Thread(target=delete, daemon=True).start()


# ---------- DECORATEUR ----------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------- AUTHENTIFICATION ----------
@app.route('/login', methods=['GET', 'POST'])

def login():

    if session.get('logged_in'):
        return redirect(url_for('form'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == os.getenv("LOGIN_USERNAME") and password == os.getenv("LOGIN_PASSWORD"):
            session['logged_in'] = True
            flash("Connexion réussie ✅", "success")
            return redirect(url_for('form'))
        else:
            flash("Identifiants incorrects ❌", "danger")
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Vous avez été déconnecté avec succès", "success",)
    return redirect(url_for('login'))


# ---------- FORMULAIRE ----------
@app.route('/form', methods=['GET', 'POST'])
def form():

    # Autorise automatiquement si accès depuis localhost
    if request.remote_addr in ['127.0.0.1', '::1']:
        session['logged_in'] = True
        print("✅ Connexion automatique activée depuis localhost")
    
    username = os.getenv("LOGIN_USERNAME", "Utilisateur")

    if request.method == 'POST':
        return generate_pdf(request)
    return render_template("form.html", username=username)

@app.route('/preview', methods=['POST'])
def preview():

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    sections = []
    i = 0
    while f'sections[{i}][title]' in request.form:
        section = {
            'title': request.form.get(f'sections[{i}][title]'),
            'instructions': request.form.get(f'sections[{i}][instructions]'),
            'questions': request.form.getlist(f'sections[{i}][questions][]'),
            'table_data': [],
            'image_url': None
        }

        # Traitement tableau CSV
        table_csv = request.form.get(f'sections[{i}][table_csv]')
        if table_csv:
            reader = csv.reader(table_csv.strip().split('\n'))
            section['table_data'] = [row for row in reader]

        # Image facultative (pas besoin de l’enregistrer ici, juste le nom suffit pour aperçu local)
        image_file = request.files.get(f'sections[{i}][image]')
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            rel_path = os.path.join("static/uploads", f"preview_{i}_{filename}")
            abs_path = os.path.join(app.root_path, rel_path)
            image_file.save(abs_path)
            delete_file_later(abs_path)
            section['image_url'] = '/' + rel_path  # pour le navigateur (HTML preview)


        sections.append(section)
        i += 1

    bareme = request.form.get("bareme")

    data = { 
        "sections": sections, 
            "bareme": bareme 
        }   
    template_choice = request.form.get("template")
    return render_template(f"{template_choice}.html", data=data)


def generate_pdf(req):
    sections = []
    i = 0
    while f'sections[{i}][title]' in req.form:
        section = {
            'title': req.form.get(f'sections[{i}][title]'),
            'instructions': req.form.get(f'sections[{i}][instructions]'),
            'questions': req.form.getlist(f'sections[{i}][questions][]'),
            'table_data': [],
            'image_url': None
        }

        table_csv = req.form.get(f'sections[{i}][table_csv]')
        if table_csv:
            reader = csv.reader(table_csv.strip().split('\n'))
            section['table_data'] = [row for row in reader]

        image_file = req.files.get(f'sections[{i}][image]')
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            rel_path = os.path.join(app.config['UPLOAD_FOLDER'], f'section_{i}_{filename}')
            abs_path = Path(rel_path).resolve()
            image_file.save(abs_path)
            section['image_url'] = f'file://{abs_path}'

        sections.append(section)
        i += 1

    bareme = req.form.get("bareme")
    data = { "sections": sections, "bareme": bareme }
    template_choice = req.form.get("template")

    # Génération du HTML
    html = render_template(f"{template_choice}.html", data=data)

    # 🧾 Création d’un fichier PDF temporaire
    temp_pdf_filename = f"fiche_{uuid.uuid4().hex}.pdf"
    temp_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_pdf_filename)

    # Création du PDF
    HTML(string=html, base_url=req.root_url).write_pdf(temp_pdf_path)

    # 🔁 Suppression automatique après 5 minutes
    delete_file_later(temp_pdf_path, delay=300)

    return send_file(temp_pdf_path, download_name="fiche_exercice.pdf", as_attachment=True)

if __name__ == '__main__':
    clean_temp_files()
    app.run(debug=True, port=8000)
