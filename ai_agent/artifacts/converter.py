import os
import subprocess

def convert_to_pdf(file_path):
    output_dir = "/tmp"
    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", output_dir, file_path],
        check=True
    )

    base_name = os.path.basename(file_path)
    pdf_path = os.path.join(output_dir, os.path.splitext(base_name)[0] + ".pdf")
    return pdf_path
