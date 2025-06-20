#!/bin/bash

# Create necessary directories
mkdir -p frontend/src/{components,hooks,utils,types,assets}
mkdir -p backend/app/{api,core,models,services,utils}
mkdir -p backend/uploads
mkdir -p backend/models

# Create placeholder files
touch backend/uploads/.gitkeep
touch backend/models/.gitkeep

# Install dependencies
npm install

# Setup frontend
cd frontend
npm install
cd ..

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..

echo "Setup complete! You can now run 'npm start' to start the development servers." 