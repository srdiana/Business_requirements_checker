# Business Requirements Checker

A powerful tool for analyzing and validating business requirements documents against templates using local LLM processing.

## Features

- Document analysis and comparison
- Support for PDF, DOCX, and TXT files
- Local LLM processing
- Real-time analysis
- Detailed error reporting

## Prerequisites

- Node.js 18+
- Python 3.9+
- 8GB RAM minimum
- 2GB free disk space

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/business-requirements-checker.git
cd business-requirements-checker
```

2. Install all dependencies:
```bash
npm run install:all
```

3. Download the ML model:
```bash
cd backend
python models/download_model.py
```

## Development

Start both frontend and backend servers:
```bash
npm start
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

## Project Structure