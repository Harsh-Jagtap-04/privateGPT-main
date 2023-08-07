from urllib.parse import quote
from urllib.parse import unquote
from flask import Flask, request, jsonify, send_from_directory
from privateGPT import initialize, serialize_document
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the directory where your PDF files are located
pdf_directory = 'source_documents'

@app.route('/query', methods=['POST'])
def ask_question():
    data = request.get_json()
    query = data['query']

    # Get the answer from the chain
    qa = initialize()
    res = qa(query)
    answer = res['result']

    docs = [serialize_document(doc) for doc in res['source_documents']]

    response_docs = []
    for doc in docs:
        file_path_parts = doc['metadata']['file_path'].split('\\')
        normalized_file_path = '/'.join(file_path_parts)  # Replace backslashes with forward slashes
        encoded_file_path = quote(normalized_file_path)  # URL-encode the path
        pdf_url = "/pdf/" + encoded_file_path

        response_doc = {
            'metadata': doc['metadata'],
            'pdf_url': pdf_url
        }
        response_docs.append(response_doc)

    response = {
        'query': query,
        'answer': answer,
        'source_documents': response_docs
    }

    return jsonify(response)

@app.route('/pdf/source_documents/<path:filename>', methods=['GET'])
def serve_pdf(filename):
    decoded_filename = unquote(filename)
    return send_from_directory(pdf_directory, decoded_filename)

if __name__ == '__main__':
    app.run(debug=True)