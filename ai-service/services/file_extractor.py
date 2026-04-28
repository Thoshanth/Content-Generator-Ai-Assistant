"""
File Extractor Service
Extracts text from PDF, DOCX, and TXT files.
"""

from typing import Optional
import io


def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """
    Extract text from uploaded file based on file type.
    
    Args:
        file_content: Raw file bytes
        filename: Original filename (used to determine file type)
    
    Returns:
        Extracted text content
    
    Raises:
        ValueError: If file type is not supported
        Exception: If extraction fails
    """
    file_ext = filename.lower().split('.')[-1]
    
    if file_ext == 'txt':
        return extract_text_from_txt(file_content)
    elif file_ext == 'pdf':
        return extract_text_from_pdf(file_content)
    elif file_ext in ['docx', 'doc']:
        return extract_text_from_docx(file_content)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")


def extract_text_from_txt(file_content: bytes) -> str:
    """Extract text from TXT file."""
    try:
        return file_content.decode('utf-8')
    except UnicodeDecodeError:
        return file_content.decode('latin-1')


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from PDF file.
    Requires PyPDF2 or pdfplumber to be installed.
    """
    try:
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except ImportError:
        raise ImportError(
            "PDF extraction requires PyPDF2. Install with: pip install PyPDF2"
        )
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_docx(file_content: bytes) -> str:
    """
    Extract text from DOCX file.
    Requires python-docx to be installed.
    """
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except ImportError:
        raise ImportError(
            "DOCX extraction requires python-docx. Install with: pip install python-docx"
        )
    except Exception as e:
        raise Exception(f"Failed to extract text from DOCX: {str(e)}")


def validate_file_size(file_size: int, max_size_mb: int = 10) -> bool:
    """
    Validate file size.
    
    Args:
        file_size: File size in bytes
        max_size_mb: Maximum allowed size in MB
    
    Returns:
        True if file is within size limit
    
    Raises:
        ValueError: If file exceeds size limit
    """
    max_bytes = max_size_mb * 1024 * 1024
    if file_size > max_bytes:
        raise ValueError(f"File size exceeds {max_size_mb}MB limit")
    return True


def validate_file_type(filename: str, allowed_types: Optional[list] = None) -> bool:
    """
    Validate file type.
    
    Args:
        filename: Original filename
        allowed_types: List of allowed file extensions (default: txt, pdf, docx, doc)
    
    Returns:
        True if file type is allowed
    
    Raises:
        ValueError: If file type is not allowed
    """
    if allowed_types is None:
        allowed_types = ['txt', 'pdf', 'docx', 'doc']
    
    file_ext = filename.lower().split('.')[-1]
    if file_ext not in allowed_types:
        raise ValueError(f"File type .{file_ext} not allowed. Allowed types: {', '.join(allowed_types)}")
    return True
