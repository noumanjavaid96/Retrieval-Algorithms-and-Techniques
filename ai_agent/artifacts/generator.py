from ai_agent.artifacts import converter
from ai_agent.artifacts import pdf_highlighter
from ai_agent.artifacts import text_highlighter

class ArtifactGenerator:
    def generate_highlighted_image(self, file_path, text_to_highlight):
        if file_path.endswith(".pdf"):
            pdf_path = file_path
            return pdf_highlighter.highlight_pdf_text(pdf_path, text_to_highlight)
        elif file_path.endswith((".docx", ".xlsx", ".pptx")):
            pdf_path = converter.convert_to_pdf(file_path)
            return pdf_highlighter.highlight_pdf_text(pdf_path, text_to_highlight)
        elif file_path.endswith((".txt", ".md", ".html")):
            return text_highlighter.highlight_text_in_image(file_path, text_to_highlight)
        else:
            return []
