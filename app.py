from flask import Flask, render_template, request, jsonify, make_response
import os
from ask_ai import ask_ai
import markdown
# from weasyprint import HTML

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_document():
    # Retrieve user info and document text from the form.
    user_name = request.form.get('name', 'User')
    email = request.form.get('email', 'user@example.com')
    document_text = request.form.get('document_text', '')

    # Check if a file was uploaded; if so, use its content.
    if 'document' in request.files:
        file = request.files['document']
        if file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                document_text = f.read()

    # Prepare a prompt that instructs the AI to process the document.
    prompt = (
        f"Process the following document for {user_name}. "
        "Remove the variables you specify, auto-fill fields using provided or public data, "
        "and generate a template ready for e-signature. "
        f"Document content: {document_text}"
    )

    # Call the AI agent (using our dummy ask_ai for now)
    result = ask_ai(prompt)
    return jsonify({'result': result})


@app.route('/explain', methods=['POST'])
def explain_terms():
    # Retrieve the legal term from the form.
    term = request.form.get('term', '')
    prompt = f"Explain in simple terms the following legal term: {term}"
    explanation = ask_ai(prompt)
    return jsonify({'explanation': explanation})


@app.route('/generate_contract', methods=['POST'])
def generate_contract():
    # Retrieve the contract description from the form.
    description = request.form.get('description', '')
    prompt = f"Write a legal contract in markdown format for the following description: {description}"

    # Ask the AI to generate the contract (in markdown format)
    markdown_content = ask_ai(prompt)

    # Convert markdown to HTML and add basic styling.
    html_body = markdown.markdown(markdown_content)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
                line-height: 1.6;
            }}
            h1, h2, h3 {{
                color: #333;
            }}
            p {{
                margin-bottom: 10px;
            }}
            ul {{
                list-style: disc;
                margin-left: 20px;
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    # Use WeasyPrint to generate a PDF from the HTML content.
    # pdf = HTML(string=html_content).write_pdf()

    # Return the PDF as a downloadable file.
    response = make_response(html_content)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=contract.pdf'
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)