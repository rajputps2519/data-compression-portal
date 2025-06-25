
# Data Compression & Decompression Portal
<p align="center">
  <a href="https://data-compression-portal-l78y.vercel.app" target="_blank">
    <img src="https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=vercel" alt="Live Demo">
  </a>
</p>


<p align="center">
  A full-stack web application built with Python (Flask) and React that allows users to compress and decompress files using various lossless algorithms.
</p>  

#### NOTE: There might be some issues in opening the site with IITR Wifi, please try opening using any other network.

---

## 🌟 Key Features

-   **Intuitive File Handling**: Modern drag-and-drop or click-to-select file upload interface.
-   **Multiple Compression Algorithms**: Implements popular lossless algorithms, including:
    -   **Run-Length Encoding (RLE)**: Best for data with long sequences of repeating characters.
    -   **Huffman Coding**: A sophisticated, frequency-based algorithm for optimal text compression.
-   **Compress & Decompress**: Seamlessly switch between compressing original files and decompressing processed files.
-   **Real-time Compression Statistics**: Instantly view detailed stats after compression, including:
    -   Original File Size
    -   Compressed File Size
    -   Compression Ratio
    -   Processing Time
-   **Download Functionality**: Easily download the processed (compressed or decompressed) files to your local machine.
-   **In-App Algorithm Explanations**: Educates users with brief, clear descriptions of how each algorithm works.
-   **Robust Error Handling**: Provides clear feedback for invalid file types, failed operations, or decompression errors.
-   **Responsive UI**: A clean and responsive user interface built with React that works smoothly on all screen sizes.

---

## 🛠️ Tech Stack

| Category      | Technology                                                                                                                                                             |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend** | ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Axios](https://img.shields.io/badge/axios-671ddf?style=for-the-badge&logo=axios&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) |
| **Backend** | ![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)                                                                                                                                                                                     |
| **Algorithms**| Custom implementations of Huffman Coding and Run-Length Encoding in pure Python.                                                                                        |
| **Deployment**| Frontend on **Vercel** / Backend on **Render**.                                                                                       |

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

You must have the following software installed:
-   [Git](https://git-scm.com/)
-   [Python 3.x](https://www.python.org/downloads/)
-   [Node.js and npm](https://nodejs.org/en/download/)


### How to Run Locally

### 1. Clone the Repository

First, clone the project from GitHub:
```bash
git clone https://github.com/rajputps2519/data-compression-portal.git
cd data-compression-portal
```

### 2. Backend Setup

1.  **Go to the backend folder:**
    ```bash
    cd backend1
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install Flask Flask-Cors python-lzma
    ```
4.  **Run the Flask backend:**
    ```bash
    python app.py
    ```
    The backend will run on `http://127.0.0.1:5000`.

### 3. Frontend Setup
1.  **Navigate to the frontend directory from the root directory (in a new terminal):**  
    ```bash
    cd frontend
    ```
2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
3.  **Run the React frontend:**
    ```bash
    npm start
    ```
    The frontend will open in your browser, usually at `http://localhost:3000`.

### Usage
1.  Ensure both the Flask backend and React frontend are running.
2.  Open your browser to `http://localhost:3000`.
3.  Upload a file, choose a compression algorithm, and click "Compress File".
4.  Download the compressed file.
5.  To decompress, upload the *compressed* file and click "Decompress File".
