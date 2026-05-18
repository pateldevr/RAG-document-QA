from pypdf import PdfReader
from pathlib import Path

def extract_text(pdf_path):
    """
    Extract Text from PDF file.
    
    Args:
    pdf_path (str): Path to the PDF file to extract text from.
    
    Return: extrated text from the PDF file.
    """

    # Check file extension
    file_path = Path(pdf_path)
    if file_path.suffix == ".pdf":
        # Load the PDF file
        try:
            reader = PdfReader(pdf_path)
            
            # Extract text from each page and join them with a newline
            full_text = "\n".join([page.extract_text() for page in reader.pages])

            return "\n".join([line for line in full_text.split("\n") if line.strip()])
        except FileNotFoundError as e:
            print(f"Error: {e}")
            raise
        except Exception as e:
            print(f"Error: {e}")
            raise
    else:
        raise ValueError("Please select correct file.")

# Usage
if __name__ == "__main__":
    text = extract_text("notice.pdf")
    print(text)
