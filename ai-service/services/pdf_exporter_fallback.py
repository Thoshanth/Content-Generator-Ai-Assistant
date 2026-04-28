"""
Fallback PDF Exporter using ReportLab
Works on Windows without external dependencies (GTK3, Cairo, Pango).
"""

from io import BytesIO
from datetime import datetime
import re

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.colors import HexColor
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def convert_markdown_to_html(text: str) -> str:
    """
    Convert markdown formatting to HTML tags for ReportLab.
    Handles bold, italic, and links.
    
    Args:
        text: Text with markdown formatting
    
    Returns:
        Text with HTML tags
    """
    # Bold: **text** -> <b>text</b>
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
    
    # Italic: *text* -> <i>text</i> (but not if it's part of **)
    text = re.sub(r'(?<!\*)\*(?!\*)([^\*]+)\*(?!\*)', r'<i>\1</i>', text)
    
    # Links: [text](url) -> <a href="url">text</a>
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    
    # Escape special XML characters
    text = text.replace('&', '&amp;')
    
    return text


def markdown_to_pdf_bytes_reportlab(markdown_content: str, content_type: str, candidate_name: str = "Document") -> bytes:
    """
    Convert markdown content to PDF using ReportLab (pure Python, no external deps).
    
    Args:
        markdown_content: Markdown-formatted content
        content_type: Type of content (resume, cover_letter, etc.)
        candidate_name: Name for the document
    
    Returns:
        PDF bytes ready for download
    
    Raises:
        ImportError: If ReportLab is not installed
        Exception: If PDF generation fails
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError(
            "ReportLab is not installed. Install with: pip install reportlab"
        )
    
    try:
        # Create PDF buffer
        buffer = BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            title=candidate_name
        )
        
        # Container for PDF elements
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#2c3e50'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=13,
            textColor=HexColor('#555555'),
            spaceAfter=6,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=HexColor('#333333'),
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            leading=14
        )
        
        bullet_style = ParagraphStyle(
            'CustomBullet',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=HexColor('#333333'),
            spaceAfter=4,
            leftIndent=20,
            bulletIndent=10,
            leading=14
        )
        
        # Parse markdown and convert to PDF elements
        lines = markdown_content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines
            if not line:
                story.append(Spacer(1, 0.1*inch))
                i += 1
                continue
            
            # H1 - Main title
            if line.startswith('# '):
                text = line[2:].strip()
                story.append(Paragraph(text, title_style))
                story.append(Spacer(1, 0.2*inch))
            
            # H2 - Section heading
            elif line.startswith('## '):
                text = line[3:].strip()
                story.append(Paragraph(text, heading_style))
            
            # H3 - Subsection
            elif line.startswith('### '):
                text = line[4:].strip()
                story.append(Paragraph(text, subheading_style))
            
            # Bullet points
            elif line.startswith('- ') or line.startswith('* '):
                text = line[2:].strip()
                # Convert markdown formatting to HTML
                text = convert_markdown_to_html(text)
                story.append(Paragraph(f'• {text}', bullet_style))
            
            # Horizontal rule
            elif line.startswith('---') or line.startswith('***'):
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph('<hr/>', body_style))
                story.append(Spacer(1, 0.1*inch))
            
            # Bold text (standalone)
            elif line.startswith('**') and line.endswith('**'):
                text = line[2:-2].strip()
                story.append(Paragraph(f'<b>{text}</b>', body_style))
            
            # Regular paragraph
            else:
                # Convert markdown formatting to HTML
                text = convert_markdown_to_html(line)
                story.append(Paragraph(text, body_style))
            
            i += 1
        
        # Add footer with generation date
        story.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=HexColor('#999999'),
            alignment=TA_CENTER
        )
        story.append(Paragraph(
            f'Generated on {datetime.now().strftime("%B %d, %Y")}',
            footer_style
        ))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        buffer.seek(0)
        return buffer.read()
    
    except Exception as e:
        raise Exception(f"PDF generation failed: {str(e)}")


def is_reportlab_available() -> bool:
    """Check if ReportLab is available."""
    return REPORTLAB_AVAILABLE
