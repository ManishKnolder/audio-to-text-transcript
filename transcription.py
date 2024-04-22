from flask import Flask, render_template, request, send_file
from langdetect import detect
from summarizer import Summarizer
import os
import whisper
from flask_weasyprint import HTML, render_pdf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    transcribed_text = result["text"]

    # Detect the language
    language = detect(transcribed_text)

    summarizer = Summarizer()
    summary = summarizer(transcribed_text)

    # Create and save PDF
    pdf_path = os.path.join('static', 'summary_output.pdf')
    create_pdf(summary, pdf_path)

    return render_template('download.html', language=language)

def create_pdf(text, filename):
    html_content = f"<html><body><p>{text}</p></body></html>"
    HTML(string=html_content).write_pdf(filename)

@app.route('/download')
def download():
    pdf_path = os.path.join('static', 'summary_output.pdf')
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
