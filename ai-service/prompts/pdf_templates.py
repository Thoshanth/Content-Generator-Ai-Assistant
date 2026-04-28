"""
PDF Templates
HTML templates for PDF export of Resume and Cover Letter.
Used by both client-side (html2pdf.js) and server-side (WeasyPrint) PDF generation.
"""


RESUME_PDF_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 11pt;
    color: #1a1a1a;
    line-height: 1.5;
    padding: 40px 50px;
    max-width: 800px;
    margin: 0 auto;
    background: #fff;
  }}
  h1 {{
    font-size: 22pt;
    font-weight: bold;
    color: #1D3557;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
  }}
  .contact-line {{
    font-size: 9pt;
    color: #555;
    margin-bottom: 18px;
    border-bottom: 2px solid #1D3557;
    padding-bottom: 10px;
  }}
  h2 {{
    font-size: 11pt;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #1D3557;
    border-bottom: 1px solid #1D3557;
    padding-bottom: 3px;
    margin-top: 18px;
    margin-bottom: 8px;
  }}
  h3 {{
    font-size: 10.5pt;
    font-weight: bold;
    color: #1a1a1a;
    margin-bottom: 1px;
  }}
  .job-meta {{
    font-size: 9.5pt;
    color: #555;
    font-style: italic;
    margin-bottom: 4px;
  }}
  ul {{
    padding-left: 16px;
    margin-bottom: 8px;
  }}
  li {{
    margin-bottom: 3px;
    font-size: 10.5pt;
  }}
  p {{
    font-size: 10.5pt;
    margin-bottom: 6px;
  }}
  .skills-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px;
    font-size: 10.5pt;
  }}
  strong {{ color: #1D3557; }}
  a {{ color: #1D3557; text-decoration: none; }}
</style>
</head>
<body>
{content}
</body>
</html>
"""


COVER_LETTER_PDF_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    color: #1a1a1a;
    line-height: 1.8;
    padding: 60px 70px;
    max-width: 800px;
    margin: 0 auto;
    background: #fff;
  }}
  .header {{
    margin-bottom: 30px;
  }}
  .sender-info {{
    font-size: 10pt;
    color: #444;
    margin-bottom: 20px;
  }}
  .date {{
    color: #666;
    margin-bottom: 20px;
    font-size: 10.5pt;
  }}
  .recipient {{
    margin-bottom: 25px;
    font-size: 10.5pt;
  }}
  p {{
    margin-bottom: 16px;
    font-size: 11pt;
  }}
  .salutation {{
    font-weight: bold;
    margin-bottom: 16px;
  }}
  .closing {{
    margin-top: 24px;
  }}
  strong {{ color: #1D3557; }}
  hr {{
    border: none;
    border-top: 1px solid #ddd;
    margin: 20px 0;
  }}
  a {{ color: #1D3557; text-decoration: none; }}
</style>
</head>
<body>
{content}
</body>
</html>
"""


def get_pdf_template(content_type: str) -> str:
    """
    Get HTML template for PDF export based on content type.
    
    Args:
        content_type: Type of content (resume, cover_letter)
    
    Returns:
        HTML template string with {content} placeholder
    """
    templates = {
        "resume": RESUME_PDF_TEMPLATE,
        "cover_letter": COVER_LETTER_PDF_TEMPLATE,
    }
    return templates.get(content_type, COVER_LETTER_PDF_TEMPLATE)
