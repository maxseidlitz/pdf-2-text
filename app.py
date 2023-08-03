import os
from flask import Flask, request, render_template
from PyPDF2 import PdfReader

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Erhalte die ausgewählten Dateien
        files = request.files.getlist('files')

        # Verzeichnis erstellen, um die PDFs hochzuladen
        upload_dir = 'uploads'
        os.makedirs(upload_dir, exist_ok=True)

        # PDFs hochladen und Text extrahieren
        extracted_text = []
        for file in files:
            filename = file.filename
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)

            with open(file_path, 'rb') as pdf_file:
                pdf = PdfReader(pdf_file)
                text = ''
                page_num = 0
                while page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    text += page.extract_text()
                    extracted_text.append((filename, text))
                    page_num += 1

        # TXT-Datei erstellen und den extrahierten Text hinzufügen
        output_file = 'output.txt'
        with open(output_file, 'w') as txt_file:
            for file, text in extracted_text:
                txt_file.write('--->' + file + '\n')
                txt_file.write(text + '\n\n')

        # Antwort an das HTML-Frontend senden
        return render_template('index.html', message='Text wurde erfolgreich extrahiert.')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)