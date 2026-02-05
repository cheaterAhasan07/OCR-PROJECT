# OCR Image Text Extraction API

A high-performance, containerized REST API built with **FastAPI** that extracts text from images using **Optical Character Recognition (OCR)**.

This project was developed as part of the **Flexbone AI Technical Challenge**. It is designed to be cloud-agnostic and production-ready using Docker.

## 🚀 Features
* **FastAPI Backend:** Asynchronous request handling for high throughput.
* **Tesseract OCR Engine:** Reliable, open-source text extraction.
* **Dockerized:** Fully containerized environment ensuring "write once, run anywhere" compatibility.
* **Confidence Scoring:** Returns an average confidence score for the extracted text.
* **Input Validation:**Strictly validates file types (JPG/PNG only) to prevent errors.

---

## 🛠️ Technology Stack
* **Language:** Python 3.9
* **Framework:** FastAPI + Uvicorn
* **OCR Engine:** Tesseract (via `pytesseract`)
* **Image Processing:** Pillow (PIL)
* **Containerization:** Docker

---

## ⚠️ Deployment Note (The "Pivot")
**Target Architecture:** Google Cloud Run + Cloud Vision API.

**Current Implementation:** Local Containerized Deployment (Tesseract).

**Context:**
Due to regional banking restrictions preventing the activation of the required Cloud Billing account (necessary for Cloud Run & Vision API), this project was pivoted to a **Local-First Containerized Architecture**.
* Instead of Cloud Vision, **Tesseract OCR** is used as the engine.
* The application is fully **Dockerized**, meaning it is ready to be deployed to Cloud Run or any Linux server immediately once infrastructure access is available.
* For the purpose of this challenge submission, the "Live Link" is provided via a secure **Ngrok Tunnel** connected to the local container.

---

## 📥 Installation & Usage

You can run this project in two ways: **Docker (Recommended)** or **Local Python**.

### Option 1: Docker (Production-Ready)
This method guarantees the environment matches exactly what was developed, isolating dependencies.

1.  **Build the Image:**
    ```bash
    docker build -t ocr-api .
    ```

2.  **Run the Container:**
    ```bash
    docker run -p 8000:8000 ocr-api
    ```

3.  **Access the API:**
    Open your browser to: `http://localhost:8000/docs`

---

### Option 2: Local Python Setup (Windows/Linux)
If you do not have Docker, you can run it directly on your machine.

**Prerequisites:**
* Python 3.9+
* **Tesseract-OCR** must be installed on your system.
    * *Windows:* [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki)
    * *Linux:* `sudo apt-get install tesseract-ocr`

**Steps:**
1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the Server:**
    ```bash
    uvicorn main:app --reload
    ```

3.  **Access the API:**
    Open `http://127.0.0.1:8000/docs`

---

## 🔌 API Endpoints

### 1. Health Check
* **GET** `/`
* **Description:** Verifies the API is active.
* **Response:** `{"message": "Local OCR API is running."}`

### 2. Extract Text
* **POST** `/extract-text`
* **Description:** Uploads an image file and returns the extracted text.
* **Body:** `multipart/form-data` (Key: `image`, Value: `[your_file.jpg]`)

**Sample Request (cURL):**
```bash
curl -X 'POST' \
  'http://localhost:8000/extract-text' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'image=@test_image.jpg;type=image/jpeg'
