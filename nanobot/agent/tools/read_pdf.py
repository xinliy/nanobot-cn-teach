"""PDF reading tool using pdfplumber."""

from nanobot.agent.tools.base import Tool


class ReadPdfTool(Tool):
    @property
    def name(self) -> str:
        return "read_pdf"

    @property
    def description(self) -> str:
        return "Extract text content from a PDF file. Use this when the user sends a PDF."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute path to the PDF file"},
            },
            "required": ["path"],
        }

    async def execute(self, path: str) -> str:
        try:
            import pdfplumber
        except ImportError:
            return "Error: pdfplumber not installed. Run: pip install pdfplumber"

        try:
            with pdfplumber.open(path) as pdf:
                pages = []
                for i, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        pages.append(f"--- Page {i} ---\n{text}")
                if not pages:
                    return "No text could be extracted from this PDF (may be image-based)."
                return "\n\n".join(pages)
        except Exception as e:
            return f"Error reading PDF: {e}"
