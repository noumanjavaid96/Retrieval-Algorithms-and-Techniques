import fitz

def highlight_pdf_text(file_path, text_to_highlight):
    doc = fitz.open(file_path)
    output_image_paths = []

    for page_num, page in enumerate(doc):
        text_instances = page.search_for(text_to_highlight)

        if text_instances:
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.update()

            pix = page.get_pixmap()
            output_image_path = f"/tmp/highlighted_page_{page_num}.png"
            pix.save(output_image_path)
            output_image_paths.append(output_image_path)

    return output_image_paths
