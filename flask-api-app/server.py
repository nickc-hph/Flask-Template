"""
Change Me
"""

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from handlers import generate_report_from_csv

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
# *** configure front-end origin here ***

@app.route('/api/', methods=['GET'])
def getReport():
    """
    Checks for the correct filetype and calls the processing handler.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    print(request.headers)
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Call the script to process the CSV file
        files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
    
        # Create the 'files' directory if it doesn't exist
        if not os.path.exists(files_dir):
            os.makedirs(files_dir)
    
        # Save the file to the 'files' directory
        file_path = os.path.join(files_dir, 'logs.csv')
        file.save(file_path)
        
        response = generate_report_from_csv()

        #pdf_path = os.path.join(files_dir, 'virtual-care-report.pdf')
        #response = send_file(pdf_path, as_attachment=True, download_name='virtual-care-report.pdf', mimetype='application/pdf')

        # Remove the files after sending the response
        os.remove(file_path)

        return response

    except FileNotFoundError as e:
        # Handle file-related errors
        return jsonify({"error": f"File not found: {str(e)}"}), 400
    except IOError as e:
        # Handle I/O errors during file processing
        return jsonify({"error": f"I/O error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
