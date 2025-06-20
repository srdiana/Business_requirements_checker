from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_processor import DocumentProcessor
from app.services.llm_analyzer import LLMAnalyzer
from app.models.response import AnalysisResponse, ErrorResponse

router = APIRouter()
document_processor = DocumentProcessor()
llm_analyzer = LLMAnalyzer()

@router.post("/process", response_model=AnalysisResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def process_documents(
    template: UploadFile = File(...),
    requirements: UploadFile = File(...)
):
    try:
        # Validate file types
        if not template.filename or not requirements.filename:
            raise HTTPException(status_code=400, detail="Both template and requirements files are required")
            
        # Process template
        template_text = await document_processor.process_file(template)
        
        # Process requirements
        requirements_text = await document_processor.process_file(requirements)
        
        # Analyze with LLM
        analysis_result = await llm_analyzer.analyze(template_text, requirements_text)
        
        return analysis_result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 