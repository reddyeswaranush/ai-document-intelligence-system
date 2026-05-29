# 📄 AI Document Intelligence System

An AI-powered document processing application that extracts structured information from PDFs and images using OCR and Large Language Models (LLMs).

The system supports scanned documents, identity cards, certificates, resumes, and other document formats. It combines image preprocessing, OCR, and AI-based information extraction to generate structured JSON outputs.

---

## 🚀 Features

### 📂 Multi-Format Support
- PDF Documents
- JPG Images
- JPEG Images
- PNG Images

### 🖼️ Image Preprocessing
- Image Resizing
- Noise Removal
- Image Sharpening
- Thresholding for improved OCR accuracy

### 🔍 OCR Extraction
- Powered by EasyOCR
- Extracts text from scanned documents
- Supports multi-page PDF processing

### 🤖 AI-Based Information Extraction
- Uses Groq LLM (Llama 3.3 70B)
- Converts raw OCR text into structured JSON
- Detects document types automatically
- Extracts relevant information dynamically

### 🪪 Aadhaar Support
- Aadhaar document detection
- Aadhaar number extraction
- Automatic Aadhaar masking for privacy

Example:

Before:

3203 3564 6737

After:

XXXX XXXX 6737

### 📊 Confidence Scoring
- Generates confidence scores for extracted fields
- Provides transparency for extracted information

### 🗃️ Document History
- Stores processed documents
- Allows viewing previously processed records

### 🛡️ Security Features
- File type validation
- File size validation
- Sensitive information masking
- Environment variable based API key management

---

# 🏗️ System Architecture

```

PDF / Image Upload
↓
Image Preprocessing
↓
EasyOCR
↓
Raw Text Extraction
↓
Groq LLM (Llama 3.3)
↓
Structured JSON Generation
↓
Confidence Scoring
↓
SQLite Storage
↓
Results Dashboard

```

---

# 🛠️ Tech Stack

## Frontend

- Streamlit

## OCR

- EasyOCR

## AI Model

- Groq API
- Llama 3.3 70B Versatile

## Image Processing

- OpenCV

## PDF Processing

- PyMuPDF

## Database

- SQLite

## Language

- Python

---

# 📁 Project Structure

```

aidoc/
│
├── app.py
│
├── services/
│ ├── preprocessing.py
│ ├── text_extractor.py
│ ├── pdf_service.py
│ ├── gemini_service.py
│ ├── confidence_service.py
│ └── database_service.py
│
├── utils/
│ └── validators.py
│
├── uploads/
├── processed/
├── database/
│
├── requirements.txt
├── .env.example
└── README.md

```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/ai-document-intelligence.git

cd ai-document-intelligence
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

## 5. Run Application

```bash
streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

# 📌 Usage

## Upload Document

Upload:

- PDF
- PNG
- JPG
- JPEG

documents through the interface.

---

## OCR Processing

The system:

1. Preprocesses the document
2. Extracts text using OCR
3. Sends extracted text to Groq LLM
4. Generates structured JSON
5. Stores results

---

## View Results

Results include:

- Document Type
- Extracted Information
- Confidence Scores
- Raw OCR Text
- Structured JSON Output

---

# 📦 Example Output

```json
{
  "document_type": "aadhaar",
  "name": null,
  "dob": null,
  "aadhaar_number": "XXXX XXXX 6737",
  "processed_at": "2026-05-29 18:42:10"
}
```

---

# 📊 Supported Document Types

- Aadhaar Card
- Resume
- Degree Certificate
- Marksheet
- Internship Posters
- Generic Documents

---

# 🔒 Security Considerations

- Sensitive Aadhaar information is masked.
- API keys are stored in environment variables.
- Uploaded files are validated before processing.
- Unsupported file formats are rejected.

---

# 🚧 Challenges Faced

## OCR Accuracy on Scanned Documents

Scanned PDFs often contain noise and distortions.

Solution:
- Resizing
- Denoising
- Sharpening
- Thresholding

---

## Structured Information Extraction

Raw OCR text is often messy.

Solution:
- LLM-based extraction using Groq
- Dynamic JSON generation

---

# 🔮 Future Improvements

Given more development time, the following improvements can be implemented:

- User Authentication
- Multi-language OCR Support
- OCR Bounding Box Visualization
- Better Aadhaar Name Extraction
- Batch Document Processing
- Cloud Database Integration
- Export Results as PDF
- Real-time OCR Confidence Dashboard
- Docker Deployment
- REST API Endpoints

---

# 🎥 Demo Video

Demo Video Link:

```text
ADD_VIDEO_LINK_HERE
```

---

# 🌐 Live Demo

Live Application:

```text
ADD_DEPLOYED_URL_HERE
```

---

# 👨‍💻 Author

Reddy Eswar Anush

CSE, NIT Agartala

AI | Machine Learning | Data Analytics Enthusiast

---