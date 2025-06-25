// Path: frontend/src/App.js

import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState(null);
  const [processedFile, setProcessedFile] = useState(null);
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');
  const [compressing, setCompressing] = useState(false);
  const [decompressing, setDecompressing] = useState(false);
  const [algorithm, setAlgorithm] = useState('rle');

  const API_URL = 'https://data-compression-portal.onrender.com';

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setUploadedFilename(selectedFile.name); // Show original filename immediately
      // Reset previous results
      setProcessedFile(null);
      setStats(null);
      setError('');
    }
  };

  const handleProcess = async (action) => {
    if (!file) {
      setError('Please select a file first.');
      return;
    }

    if (action === 'compress') {
      setCompressing(true);
    } else {
      setDecompressing(true);
    }
    setError('');
    setProcessedFile(null);
    setStats(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Step 1: Always upload the original file first
      const uploadRes = await axios.post(`${API_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      const filenameToProcess = uploadRes.data.filename;

      let processRes;
      if (action === 'compress') {
        // Step 2: Call compress endpoint
        processRes = await axios.post(`${API_URL}/compress/${algorithm}/${filenameToProcess}`);
        setStats({
          original_size: processRes.data.original_size,
          compressed_size: processRes.data.compressed_size,
          compression_ratio: processRes.data.compression_ratio,
          processing_time: processRes.data.processing_time,
        });
      } else { // Decompress
        // Step 2: Call decompress endpoint
        processRes = await axios.post(`${API_URL}/decompress/${filenameToProcess}`);
        setStats(null); // No stats for decompression in this setup
      }
      setProcessedFile(processRes.data.filename);

    } catch (err) {
      const errorMessage = err.response ? err.response.data.error : `An error occurred during ${action}.`;
      setError(errorMessage);
      console.error(err);
    } finally {
      if (action === 'compress') {
        setCompressing(false);
      } else {
        setDecompressing(false);
      }
    }
  };

  const handleDownload = () => {
    if (!processedFile) return;
    window.open(`${API_URL}/download/${processedFile}`);
  };

  const loading = compressing || decompressing;

  return (
    <div className="App">
      <header className="App-header">
        <h1>Data Compression & Decompression Portal</h1>
        <p>A Python + React demonstration</p>
      </header>
      <main>
        <div className="card">
          <h2>1. Select Your File</h2>
          <input type="file" onChange={handleFileChange} />
          {uploadedFilename && <p className="file-info">Selected: {uploadedFilename}</p>}
        </div>

        <div className="card">
          <h2>2. Choose Algorithm & Process</h2>
          <div className="controls">
            <select value={algorithm} onChange={(e) => setAlgorithm(e.target.value)} disabled={loading}>
              <option value="rle">Run-Length Encoding (RLE)</option>
              <option value="huffman">Huffman Coding</option>
            </select>
            <button onClick={() => handleProcess('compress')} disabled={loading || !file}>
              {compressing ? 'Compressing...' : 'Compress'}
            </button>
            <button onClick={() => handleProcess('decompress')} disabled={loading || !file}>
              {decompressing ? 'Decompressing...' : 'Decompress'}
            </button>
          </div>
        </div>

        {error && <p className="error-message">{error}</p>}
        {(compressing || decompressing) && <div className="loader"></div>}

        {stats && processedFile && (
          <div className="card results-card">
            <h2>Compression Results</h2>
            <div className="stats-grid">
              <p><strong>Original Size:</strong> {stats.original_size} bytes</p>
              <p><strong>Compressed Size:</strong> {stats.compressed_size} bytes</p>
              <p><strong>Ratio:</strong> {stats.compression_ratio}:1</p>
              <p><strong>Time:</strong> {stats.processing_time}</p>
            </div>
            <div className="download-section">
              <span>{processedFile}</span>
              <button onClick={handleDownload}>Download</button>
            </div>
          </div>
        )}

        {!stats && processedFile && (
           <div className="card results-card">
           <h2>Decompression Complete</h2>
           <div className="download-section">
             <span>{processedFile}</span>
             <button onClick={handleDownload}>Download</button>
           </div>
         </div>
        )}

        <div className="card-group">
          <div className="card info-card">
            <h3>Run-Length Encoding (RLE)</h3>
            <p>A simple, lossless compression method that works well for data with many consecutive repeating values (runs). It stores the value and the count of its repetition. For example, `AAAAABB` becomes `5A2B`.</p>
          </div>
          <div className="card info-card">
            <h3>Huffman Coding</h3>
            <p>A sophisticated, lossless compression algorithm. It analyzes the frequency of each character (or byte) and assigns shorter binary codes to more frequent characters and longer codes to less frequent ones, resulting in a smaller overall file size.</p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
