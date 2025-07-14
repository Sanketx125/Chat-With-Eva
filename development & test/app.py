from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import fitz  # from PyMuPDF
import storage as s
from engine import main_chain

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PDF_TEXT'] = ""

# Store the last AI response




os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():

    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF uploaded'}), 400

    s.pdf_file = request.files['pdf']
    filename = secure_filename(s.pdf_file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    s.pdf_file.save(path)

    # Extract text from the PDF using PyMuPDF
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()

    app.config['PDF_TEXT'] = text
    return jsonify({'message': 'PDF uploaded and processed successfully.'})


@app.route('/chat', methods=['POST'])
def chat():
    s.user_message = request.json.get('message', '')

    if not app.config['PDF_TEXT']:
        s.ai_response = "❗Please upload a PDF first."
        return jsonify({'response': s.ai_response})

    s.ai_response = main_chain.invoke(s.user_message)
    return jsonify({'response': s.ai_response})

if __name__ == '__main__':
    app.run(debug=True)
