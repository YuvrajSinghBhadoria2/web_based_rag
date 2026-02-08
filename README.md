---
title: Web-Based RAG System
emoji: 📚
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Web-Based RAG System

A production-ready Retrieval-Augmented Generation (RAG) system that combines PDF document processing and web search capabilities to provide intelligent answers to user queries.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Frontend Components](#frontend-components)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Multi-Modal Query Processing**: Supports queries against both uploaded PDF documents and live web search
- **PDF Document Management**: Upload, store, and process PDF documents with advanced extraction techniques
- **OCR Support for Scanned PDFs**: Automatically extracts text from image-based/scanned PDFs using Tesseract OCR
- **Hybrid Search**: Combine PDF-based retrieval with web search for comprehensive answers
- **Confidence Scoring**: Provides confidence scores for generated responses
- **Vector Storage**: Efficient similarity search using ChromaDB vector database
- **Modern UI**: Responsive React-based frontend with intuitive user experience
- **RESTful API**: Well-documented API endpoints for easy integration
- **File Upload**: Drag-and-drop PDF upload functionality
- **Query Modes**: Different query modes (PDF-only, Web-only, Hybrid, Restricted)

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: ChromaDB (Vector Database)
- **Embeddings**: Sentence Transformers
- **Language**: Python 3.11+
- **Web Framework**: FastAPI with Uvicorn ASGI server
- **HTTP Client**: aiohttp
- **PDF Processing**: PyPDF, pdfplumber, pdf2image, pytesseract
- **OCR**: Tesseract for scanned/image-based PDFs
- **LLM Integration**: Groq API
- **Environment Management**: python-dotenv
- **Data Validation**: Pydantic

### Frontend
- **Framework**: React 18+
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **UI Components**: Custom-built with Lucide React icons
- **File Upload**: react-dropzone
- **Notifications**: react-hot-toast

## Architecture

The application follows a microservices architecture with a clear separation between frontend and backend:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   Services      │
│                 │    │                 │    │                 │
│ • User Interface│    │ • API Gateway   │    │ • Groq API      │
│ • File Upload   │    │ • PDF Processor │    │ • Web Search    │
│ • Query Input   │    │ • Embedding     │    │ • Vector Store  │
│ • Results Display│   │ • Retriever     │    │                 │
└─────────────────┘    │ • LLM Service   │    └─────────────────┘
                       └─────────────────┘
```

## Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn
- Git
- **Tesseract OCR** (for scanned PDF support):
  - macOS: `brew install tesseract poppler`
  - Ubuntu: `sudo apt-get install tesseract-ocr poppler-utils`
  - Windows: Download from https://github.com/tesseract-ocr/tesseract

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YuvrajSinghBhadoria2/web_based_rag.git
   cd web_based_rag/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory based on `.env.bak`:
   ```bash
   cp .env.bak .env
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Configuration

### Backend Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here  # Optional - for web search
TAVILY_API_KEY=your_tavily_api_key_here  # Optional - for web search
CHROMA_DB_PATH=./storage/vector_db
UPLOAD_DIR=./storage/uploads
MODEL_NAME=llama3-70b-8192
TEMPERATURE=0.1
MAX_TOKENS=1000
TOP_P=1
STOP_TOKENS=["\n", "###"]
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000", "http://localhost:5175"]
```

Replace `your_groq_api_key_here` with your actual Groq API key. You can get one from [Groq Cloud](https://console.groq.com/keys).

For web search functionality, add Serper or Tavily API keys (optional - without them, hybrid mode will only use PDF sources).

## Usage

### Running the Backend

1. Make sure you're in the backend directory
2. Activate your virtual environment
3. Start the backend server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The backend will be available at `http://localhost:8000` with API documentation at `http://localhost:8000/api/docs`.

### Running the Frontend

1. Navigate to the frontend directory
2. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`.

### Application Workflow

1. **Upload Documents**: Use the drag-and-drop interface to upload PDF documents
2. **Select Query Mode**: Choose between PDF-only, Web-only, Hybrid, or Restricted modes
3. **Enter Query**: Type your question in the query input
4. **Get Response**: Receive an AI-generated answer with confidence score and source citations
5. **Review Sources**: View the documents and web pages that contributed to the response

### OCR for Scanned PDFs

The system automatically detects and processes scanned/image-based PDFs using Tesseract OCR:
- If a PDF contains selectable text, it uses the native text extraction
- If no text is found, it automatically applies OCR to extract text from images
- Works with scanned documents, image-only PDFs, and documents with mixed content

## Project Structure

```
web_based_rag/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── routes/
│   │   │           ├── documents.py    # Document management endpoints
│   │   │           ├── health.py       # Health check endpoint
│   │   │           ├── query.py        # Query processing endpoints
│   │   │           └── upload.py       # File upload endpoints
│   │   ├── core/     # Core utilities and configurations
│   │   ├── models/
│   │   │   └── schemas.py              # Pydantic models and schemas
│   │   ├── services/
│   │   │   ├── confidence.py          # Confidence scoring service
│   │   │   ├── embeddings.py          # Embedding generation service
│   │   │   ├── enhanced_llm.py        # Enhanced LLM service
│   │   │   ├── llm_service.py         # LLM integration service
│   │   │   ├── pdf_processor.py       # PDF processing service
│   │   │   ├── prompt_guard.py        # Prompt safety service
│   │   │   ├── retriever.py           # Information retrieval service
│   │   │   ├── vector_store.py        # Vector database operations
│   │   │   └── web_search.py          # Web search service
│   │   ├── utils/
│   │   │   ├── chunking.py           # Text chunking utilities
│   │   │   └── rate_limiter.py        # Rate limiting utilities
│   │   ├── config.py                 # Configuration settings
│   │   └── main.py                   # Application entry point
│   ├── storage/
│   │   ├── uploads/                  # Uploaded PDF files
│   │   ├── vector_db/                # Vector database files
│   │   └── documents.json            # Document metadata
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Docker configuration
│   └── .env.bak                      # Environment variables template
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── common/               # Reusable UI components
    │   │   ├── documents/            # Document-related components
    │   │   ├── layout/               # Layout components
    │   │   ├── query/                # Query input components
    │   │   ├── results/              # Results display components
    │   │   └── settings/             # Settings modal components
    │   ├── context/
    │   │   └── AppContext.tsx        # Application state management
    │   ├── services/
    │   │   └── api.ts                # API service client
    │   ├── types/
    │   │   └── index.ts              # Type definitions
    │   ├── App.tsx                   # Main application component
    │   └── main.tsx                  # Application entry point
    ├── package.json
    ├── tsconfig.json
    ├── tailwind.config.js
    └── vite.config.ts
```

## API Endpoints

### Health Check
- `GET /` - Root endpoint returning API information

### Documents
- `GET /api/v1/documents` - Get list of uploaded documents
- `DELETE /api/v1/documents/{document_id}` - Delete a document

### File Upload
- `POST /api/v1/upload` - Upload PDF document

### Query
- `POST /api/v1/query` - Process query with specified mode
  - Request body: `{"query": "your query", "mode": "pdf|web|hybrid|restricted", "document_ids": ["optional document IDs"]}`
  - Response: `{"response": "answer", "sources": [], "confidence": 0.85}`

### Additional Endpoints
- `GET /api/docs` - Interactive API documentation (Swagger UI)
- `GET /api/redoc` - Alternative API documentation (ReDoc)

## Frontend Components

### Layout Components
- **Header**: Navigation and branding
- **Sidebar**: Document management and settings
- **MainContent**: Primary content area

### Document Components
- **FileUpload**: Drag-and-drop PDF upload
- **DocumentList**: Display of uploaded documents
- **DocumentCard**: Individual document information

### Query Components
- **QueryInput**: Input field with mode selector
- **ModeSelector**: Options for PDF-only, Web-only, Hybrid, or Restricted queries

### Results Components
- **ResultsDisplay**: Container for query results
- **AnswerCard**: Display of the AI-generated answer
- **SourcesList**: List of source documents
- **SourceCard**: Detailed source information
- **ConfidenceIndicator**: Visual representation of response confidence

### Settings Components
- **SettingsModal**: Configuration options

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Deploying to Hugging Face Spaces

This application is configured for deployment on Hugging Face Spaces using the Docker SDK. The repository includes:

- A `Dockerfile` that sets up the complete environment
- A `README.md` with proper Hugging Face metadata
- All necessary backend and frontend code

To deploy to your Space:

1. Create a new Space with the Docker SDK
2. Point it to this repository
3. Add your API keys as Space Secrets:
   - `GROQ_API_KEY`: Your Groq API key
4. The Space will automatically build and deploy using the Dockerfile

Your application will be served at the port specified in the Dockerfile (7860).

### Option 1: Using the Docker Image

1. Create a new Space on Hugging Face with the following settings:
   - **Space SDK**: Docker
   - **Hardware**: Choose based on your needs (GPU recommended for better performance)

2. Add your Hugging Face token and API keys as secrets in the Space settings:
   - `HF_TOKEN`: Your Hugging Face token (`your_hf_token_here`)
   - `GROQ_API_KEY`: Your Groq API key
   - Any other required API keys

3. Create a `Dockerfile` in your Space repository with the following content:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install nodejs for the frontend
RUN apt-get update && apt-get install -y nodejs npm && apt-get clean

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install frontend dependencies
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm ci --only=production

# Copy the rest of the application
COPY . .

# Build the frontend
RUN cd frontend && npm run build

# Expose the port Hugging Face Spaces expects
EXPOSE 7860

# Start both backend and frontend
CMD bash -c "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 7860 & cd frontend && npx serve -s dist -l 7861"
```

4. Create an `.env` file in the backend directory with your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
# Add other required environment variables
```

### Option 2: Deploying Your Existing React Frontend (Recommended)

To deploy your existing React frontend along with the FastAPI backend (this preserves your original UI):

1. In your Hugging Face Space repository, copy your entire project

2. Create a Dockerfile that builds and serves both applications:

```dockerfile
FROM node:18-alpine AS frontend-build
WORKDIR /app
COPY frontend/package*.json .
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM python:3.11-slim AS backend-build
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Copy built frontend
COPY --from=frontend-build /app/dist ./frontend/dist

# Install node for serving frontend
RUN apt-get update && apt-get install -y nodejs npm && apt-get clean

EXPOSE 7860

CMD python -m uvicorn app.main:app --host 0.0.0.0 --port 7860
```

3. Update your backend CORS settings in `backend/app/config.py` to allow the Hugging Face Space URL

4. Add your API keys as Space secrets:
   - `GROQ_API_KEY`: Your Groq API key
   - Other required API keys

Note: This approach maintains your original React interface which is more feature-rich than a Gradio interface. Your existing frontend with its document cards, sidebar, settings modal, and responsive design will be preserved.

## Deployment Steps

1. Create a new repository on Hugging Face Spaces
2. Push your code to the repository
3. Add your API keys as secrets in the Space settings
4. The application will automatically build and deploy

Your RAG application is now ready for deployment on Hugging Face Spaces with your Hugging Face token: `your_hf_token_here`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
