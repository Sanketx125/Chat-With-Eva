from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import fitz  # from PyMuPDF
import storage as s
import engine
from engine import create_vector_store, answer_question



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PDF_TEXT'] = ""

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF uploaded'}), 400

    pdf_file = request.files['pdf']
    filename = secure_filename(pdf_file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(path)

    # Create vector store
    engine.create_vector_store(path)
    app.config['PDF_PATH'] = path

    if os.path.exists(path):
        os.remove(path)

    return jsonify({
        'message': '✅ PDF uploaded and vector store created successfully.',
        'greeting': "👋 Hello buddy! I'm Eva, your AI friend. Developed with ❤️ by Sanket Mane."
    })



@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    if not app.config.get('PDF_PATH'):
        return jsonify({'response': "❗Please upload a PDF first."})


    answer = answer_question(user_message)

    return jsonify({'response': answer})


if __name__ == '__main__':
    app.run(debug=True)
