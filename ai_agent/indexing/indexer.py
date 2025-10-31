from ai_agent.gdrive.client import GDriveClient
from ai_agent.parsers import pdf_parser, docx_parser, xlsx_parser, pptx_parser, text_parsers
from ai_agent.vector_store.db import VectorStore

class Indexer:
    def __init__(self):
        self.gdrive_client = GDriveClient()
        self.vector_store = VectorStore()
        self.status = "Not started"
        self.file_map = {}

    def run_full_index(self):
        self.status = "Connecting to Google Drive"
        files = self.gdrive_client.list_files()

        total_files = len(files)
        for i, file in enumerate(files):
            self.status = f"Indexing {i+1}/{total_files} docs"
            file_id = file.get('id')
            file_name = file.get('name')
            mime_type = file.get('mimeType')

            # Download the file
            downloaded_path = self.gdrive_client.download_file(file_id, f"data/{file_name}", mime_type)

            if downloaded_path:
                self.file_map[file_id] = downloaded_path
                # Parse the file
                text = self._parse_file(downloaded_path, mime_type)

                # Add to vector store
                if text:
                    self.vector_store.add_document(doc_id=file_id, text=text)

        self.status = "Complete"

    def _parse_file(self, file_path, mime_type):
        if ".pdf" in file_path:
            return pdf_parser.parse_pdf(file_path)
        elif ".docx" in file_path:
            return docx_parser.parse_docx(file_path)
        elif ".xlsx" in file_path:
            return xlsx_parser.parse_xlsx(file_path)
        elif ".pptx" in file_path:
            return pptx_parser.parse_pptx(file_path)
        elif ".txt" in file_path:
            return text_parsers.parse_txt(file_path)
        elif ".md" in file_path:
            return text_parsers.parse_md(file_path)
        elif ".html" in file_path:
            return text_parsers.parse_html(file_path)
        return None

    def get_status(self):
        return self.status

    def get_file_path(self, doc_id):
        return self.file_map.get(doc_id)
