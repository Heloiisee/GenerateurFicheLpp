from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
from weasyprint import HTML
from io import BytesIO
import csv
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        return generate_pdf(request)
    return render_template("form.html")

@app.route('/preview', methods=['POST'])
def preview():
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

    bareme = request.form.get("bareme")

    data = { 
        "sections": sections, 
            "bareme": bareme 
        }   
    template_choice = req.form.get("template")

    html = render_template(f"{template_choice}.html", data=data)
    pdf_file = BytesIO()
    HTML(string=html, base_url=req.root_url).write_pdf(pdf_file)
    pdf_file.seek(0)
    return send_file(pdf_file, download_name="fiche_exercice.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
