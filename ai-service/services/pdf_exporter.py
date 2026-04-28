"""
PDF Exporter Service
Server-side PDF generation using WeasyPrint (preferred) or ReportLab (fallback).
Converts markdown AI output to styled PDF.
"""

from io import BytesIO

# Check WeasyPrint availability (may fail if GTK3 not installed)
WEASYPRINT_AVAILABLE = False
try:
    import markdown as md
    from weasyprint import HTML, CSS
    from prompts.pdf_templates import get_pdf_template
    WEASYPRINT_AVAILABLE = True
except Exception as e:
    # WeasyPrint import failed (missing GTK3 or other dependencies)
    print(f"[PDF Export] WeasyPrint not available: {e}")
    WEASYPRINT_AVAILABLE = False

# Check ReportLab availability (fallback)
REPORTLAB_AVAILABLE = False
try:
    from services.pdf_exporter_fallback import markdown_to_pdf_bytes_reportlab, is_reportlab_available
    REPORTLAB_AVAILABLE = is_reportlab_available()
    if REPORTLAB_AVAILABLE:
        print("[PDF Export] ReportLab available as fallback")
except ImportError as e:
    print(f"[PDF Export] ReportLab not available: {e}")
    REPORTLAB_AVAILABLE = False


def markdown_to_pdf_bytes(markdown_content: str, content_type: str, candidate_name: str = "Document") -> bytes:
    """
    Convert markdown AI output → styled HTML → PDF bytes.
    Uses WeasyPrint if available, falls back to ReportLab on Windows.
    Returns raw PDF bytes for streaming to client.
    
    Args:
        markdown_content: Markdown-formatted content
        content_type: Type of content (resume, cover_letter)
        candidate_name: Name for the document (used in fallback)
    
    Returns:
        PDF bytes ready for download
    
    Raises:
        ImportError: If neither WeasyPrint nor ReportLab is installed
        Exception: If PDF generation fails
    """
    # Try WeasyPrint first (better quality)
    if WEASYPRINT_AVAILABLE:
        try:
            # Step 1: markdown → HTML body
            html_body = md.markdown(
                markdown_content,
                extensions=["extra", "nl2br", "sane_lists"]
            )

            # Step 2: Inject into styled template
            template = get_pdf_template(content_type)
            full_html = template.format(content=html_body)

            # Step 3: WeasyPrint renders HTML → PDF
            pdf_bytes = BytesIO()
            HTML(string=full_html).write_pdf(pdf_bytes)
            pdf_bytes.seek(0)
            return pdf_bytes.read()
        
        except Exception as e:
            # If WeasyPrint fails (missing GTK3), try fallback
            print(f"[PDF Export] WeasyPrint generation failed: {e}")
            if REPORTLAB_AVAILABLE:
                print("[PDF Export] Falling back to ReportLab...")
                return markdown_to_pdf_bytes_reportlab(markdown_content, content_type, candidate_name)
            raise Exception(f"PDF generation failed: {str(e)}")
    
    # Fallback to ReportLab (works on Windows without GTK3)
    elif REPORTLAB_AVAILABLE:
        print("[PDF Export] Using ReportLab (WeasyPrint not available)")
        return markdown_to_pdf_bytes_reportlab(markdown_content, content_type, candidate_name)
    
    # Neither library available
    else:
        raise ImportError(
            "PDF export requires either WeasyPrint or ReportLab.\n"
            "Install ReportLab: pip install reportlab (recommended for Windows)\n"
            "Or install WeasyPrint: pip install weasyprint (requires GTK3 on Windows)"
        )
