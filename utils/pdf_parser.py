import PyPDF2
from io import BytesIO

class PDFParser:
    def __init__(self):
        """Initialize the PDF parser"""
        pass
        
    def parse_pdf(self, file_stream):
        """
        Extract text from a PDF file
        
        Args:
            file_stream: A file-like object containing the PDF
            
        Returns:
            str: Extracted text from the PDF
        """
        try:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_stream.read()))
            
            # Extract text from all pages
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"
            
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return f"Error extracting text: {str(e)}"