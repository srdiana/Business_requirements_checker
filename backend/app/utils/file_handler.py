import os
import aiofiles
import magic
from fastapi import UploadFile, HTTPException
from pathlib import Path
from ..core.config import settings

class FileHandler:
    @staticmethod
    async def save_upload_file(upload_file: UploadFile) -> Path:
        try:
            if not upload_file.filename:
                raise HTTPException(status_code=400, detail="No file provided")
            
            # Create upload directory if it doesn't exist
            settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            file_path = settings.UPLOAD_DIR / f"{upload_file.filename}"
            
            # Check if file already exists
            if file_path.exists():
                raise HTTPException(status_code=400, detail="File with this name already exists")
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as out_file:
                content = await upload_file.read()
                if len(content) > settings.MAX_UPLOAD_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes"
                    )
                await out_file.write(content)
            
            return file_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    @staticmethod
    def validate_file_type(file_path: Path) -> str:
        try:
            mime = magic.from_file(str(file_path), mime=True)
            if mime not in {
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "text/plain"
            }:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {mime}"
                )
            return mime
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error validating file: {str(e)}")

    @staticmethod
    async def cleanup_file(file_path: Path):
        try:
            if file_path.exists():
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {str(e)}") 