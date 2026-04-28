"""
Tools Router
Endpoints for export, PDF generation, follow-up questions, and utility functions.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from models.schemas import ExportRequest, ExportResponse, PdfExportRequest, FollowUpRequest, FollowUpResponse
from services.export_service import to_plain_text, to_html, to_markdown, word_count, char_count
from services.followup_service import generate_followup_questions

router = APIRouter(prefix="/tools", tags=["tools"])


@router.post("/export", response_model=ExportResponse)
async def export_content(req: ExportRequest):
    """
    Convert AI markdown output to requested text format.
    Supports: plain_text, html, markdown
    
    Args:
        req: ExportRequest with content, format, and content_type
    
    Returns:
        ExportResponse with converted content and statistics
    """
    try:
        if req.format == "plain_text":
            converted = to_plain_text(req.content)
        elif req.format == "html":
            converted = to_html(req.content)
        else:  # markdown
            converted = to_markdown(req.content)

        return ExportResponse(
            content=converted,
            format=req.format,
            word_count=word_count(converted),
            char_count=char_count(converted)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.post("/export-pdf")
async def export_pdf(req: PdfExportRequest):
    """
    Convert AI markdown output to a downloadable PDF.
    Used for Resume and Cover Letter.
    Returns PDF bytes with correct headers for browser download.
    
    Supports both WeasyPrint (preferred) and ReportLab (fallback for Windows).
    
    Args:
        req: PdfExportRequest with content, content_type, and candidate_name
    
    Returns:
        PDF file as binary response
    """
    try:
        # Import PDF exporter (with fallback support)
        try:
            from services.pdf_exporter import markdown_to_pdf_bytes
        except ImportError:
            raise HTTPException(
                status_code=503,
                detail="PDF export service not available. Install either: pip install weasyprint OR pip install reportlab"
            )
        
        # Generate PDF with candidate name
        pdf_bytes = markdown_to_pdf_bytes(
            req.content, 
            req.content_type,
            req.candidate_name or "Document"
        )

        filename_map = {
            "resume":       f"{req.candidate_name or 'resume'}_resume.pdf",
            "cover_letter": f"{req.candidate_name or 'cover_letter'}.pdf",
        }
        filename = filename_map.get(req.content_type, "document.pdf")
        
        # Sanitize filename (remove special characters)
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).strip()

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(len(pdf_bytes))
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")


@router.post("/followup-questions", response_model=FollowUpResponse)
async def get_followup_questions(req: FollowUpRequest):
    """
    Generate intelligent follow-up questions based on content type and initial input.
    Helps gather all necessary information before generating content.
    
    Args:
        req: FollowUpRequest with content_type, initial content (optional), and user_id
    
    Returns:
        FollowUpResponse with list of 3-8 follow-up questions
    """
    try:
        questions = await generate_followup_questions(
            content_type=req.content_type.value,
            initial_prompt=req.content,
            user_id=req.user_id
        )
        
        return FollowUpResponse(
            questions=questions,
            content_type=req.content_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate follow-up questions: {str(e)}")
