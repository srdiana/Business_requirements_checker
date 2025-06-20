import io
import os
from fastapi import UploadFile, HTTPException
from pdfminer.high_level import extract_text
from docx import Document
import magic
import aiofiles
from typing import Optional
from pathlib import Path
from ..utils.file_handler import FileHandler

class DocumentProcessor:
    SUPPORTED_MIME_TYPES = {
        "application/pdf": ".pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        "text/plain": ".txt"
    }

    def __init__(self):
        self.file_handler = FileHandler()

    async def process_file(self, upload_file: UploadFile) -> str:
        try:
            if not upload_file.filename:
                raise HTTPException(status_code=400, detail="No file provided")
            
            # Save file
            file_path = await self.file_handler.save_upload_file(upload_file)
            
            try:
                # Validate file type
                mime_type = self.file_handler.validate_file_type(file_path)
                
                # Process based on file type
                if mime_type == "application/pdf":
                    text = self._process_pdf(file_path)
                elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = self._process_docx(file_path)
                else:  # text/plain
                    async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                        text = await f.read()
                
                if not text.strip():
                    raise HTTPException(status_code=400, detail="File is empty")
                
                return text
            finally:
                # Clean up file
                await self.file_handler.cleanup_file(file_path)
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
    def _process_pdf(self, file_path: Path) -> str:
        try:
            return extract_text(str(file_path))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    def _process_docx(self, file_path: Path) -> str:
        try:
            doc = Document(str(file_path))
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing DOCX: {str(e)}") 