"""
Document reading service for different file types
"""

import os
from typing import Optional

class DocumentReader:
    """Read content from different document types"""
    
    @staticmethod
    def read_document(file_path: str, file_type: str) -> str:
        """Read document content based on file type"""
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Handle PDF files
        if file_type and 'pdf' in file_type.lower():
            return DocumentReader._read_pdf(file_path)
        
        # Handle DOCX files
        elif file_type and 'word' in file_type.lower() or file_path.lower().endswith('.docx'):
            return DocumentReader._read_docx(file_path)
        
        # Handle text files
        elif file_type and 'text' in file_type.lower() or file_path.lower().endswith('.txt'):
            return DocumentReader._read_text(file_path)
        
        # Default: try to read as text
        else:
            try:
                return DocumentReader._read_text(file_path)
            except:
                raise ValueError(f"Unsupported file type: {file_type}")
    
    @staticmethod
    def _read_pdf(file_path: str) -> str:
        """Read PDF file content"""
        try:
            import PyPDF2
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text.strip()
                
        except ImportError:
            raise ImportError("PyPDF2 is required for PDF processing. Install with: pip install PyPDF2")
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    @staticmethod
    def _read_docx(file_path: str) -> str:
        """Read DOCX file content"""
        try:
            from docx import Document
            
            doc = Document(file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
            
        except ImportError:
            raise ImportError("python-docx is required for DOCX processing. Install with: pip install python-docx")
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    @staticmethod
    def _read_text(file_path: str) -> str:
        """Read text file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")
