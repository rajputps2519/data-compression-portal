# Path: backend/app.py

import os
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Import our algorithm functions
from algorithms.rle import encode_rle, decode_rle
from algorithms.huffman import encode_huffman, decode_huffman

# Create the Flask app
app = Flask(__name__)

# The URL of your live Vercel frontend application
frontend_url = "https://data-compression-portal-l78y.vercel.app"

# Configure CORS to only allow requests from your specific frontend
CORS(app, origins=[frontend_url, frontend_url + '/'])

# Configure an upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename})


@app.route('/compress/<algorithm>/<filename>', methods=['POST'])
def compress_file(algorithm, filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    with open(file_path, 'rb') as f:
        data = f.read()

    start_time = time.time()
    
    try:
        if algorithm == 'rle':
            compressed_data = encode_rle(data)
        elif algorithm == 'huffman':
            compressed_data = encode_huffman(data)
        else:
            return jsonify({'error': 'Invalid algorithm'}), 400
    except Exception as e:
        return jsonify({'error': f'Compression failed: {str(e)}'}), 500

    processing_time = time.time() - start_time

    base, ext = os.path.splitext(filename)
    compressed_filename = f"{base}_{algorithm}_compressed{ext}"
    compressed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], compressed_filename)
    
    with open(compressed_file_path, 'wb') as f:
        f.write(compressed_data)

    original_size = os.path.getsize(file_path)
    compressed_size = os.path.getsize(compressed_file_path)
    compression_ratio = original_size / compressed_size if compressed_size != 0 else float('inf')

    return jsonify({
        'message': 'File compressed successfully',
        'filename': compressed_filename,
        'original_size': original_size,
        'compressed_size': compressed_size,
        'compression_ratio': f'{compression_ratio:.2f}',
        'processing_time': f'{processing_time:.4f} seconds'
    })


@app.route('/decompress/<filename>', methods=['POST'])
def decompress_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    with open(file_path, 'rb') as f:
        data = f.read()
    
    try:
        parts = filename.rsplit('_', 2)
        base_name, algorithm, _ = parts
    except ValueError:
        return jsonify({'error': 'Invalid compressed filename format. Expected format: <name>_<algorithm>_compressed.<ext>'}), 400

    start_time = time.time()
    try:
        if algorithm == 'rle':
            decompressed_data = decode_rle(data)
        elif algorithm == 'huffman':
            decompressed_data = decode_huffman(data)
        else:
            return jsonify({'error': f'Unknown algorithm for decompression: {algorithm}'}), 400
    except Exception as e:
        return jsonify({'error': f'Decompression failed: {str(e)}'}), 500
        
    processing_time = time.time() - start_time
    
    original_base, _, _ = os.path.splitext(filename)[0].rsplit('_', 2)
    decompressed_filename = f"{original_base}_decompressed{os.path.splitext(filename)[1]}"
    decompressed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], decompressed_filename)
    
    with open(decompressed_file_path, 'wb') as f:
        f.write(decompressed_data)

    return jsonify({
        'message': 'File decompressed successfully',
        'filename': decompressed_filename,
        'processing_time': f'{processing_time:.4f} seconds'
    })


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
