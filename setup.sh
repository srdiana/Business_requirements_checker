#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required tools
echo "Checking required tools..."

if ! command_exists python3; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

if ! command_exists npm; then
    echo "npm is not installed. Please install Node.js and npm first."
    exit 1
fi

# Create project structure
echo "Creating project structure..."

# Create directories
mkdir -p frontend/src/{components,hooks,utils,types,assets}
mkdir -p backend/app/{api,core,models,services,utils}
mkdir -p backend/uploads
mkdir -p backend/models

# Create backend files
echo "Setting up backend..."
python3 -m venv backend/venv
source backend/venv/bin/activate

# Install backend dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt

# Create .gitkeep files
touch backend/uploads/.gitkeep
touch backend/models/.gitkeep

# Setup frontend
echo "Setting up frontend..."
cd frontend

# Clean install of frontend dependencies
rm -rf node_modules package-lock.json
npm install

# Fix security vulnerabilities
npm audit fix

cd ..

echo "Setup complete! You can now run the development servers:"
echo "1. Start backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "2. Start frontend: cd frontend && npm run dev" 