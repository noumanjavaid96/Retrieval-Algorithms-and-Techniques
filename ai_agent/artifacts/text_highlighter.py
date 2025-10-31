from PIL import Image, ImageDraw, ImageFont

def highlight_text_in_image(file_path, text_to_highlight):
    with open(file_path, 'r') as f:
        content = f.read()

    font = ImageFont.load_default()

    # Create a dummy image to get the text size
    dummy_img = Image.new('RGB', (0, 0))
    dummy_draw = ImageDraw.Draw(dummy_img)
    text_bbox = dummy_draw.textbbox((0, 0), content, font=font)
    text_width = text_bbox[2]
    text_height = text_bbox[3]

    img = Image.new('RGB', (text_width + 20, text_height + 20), color = 'white')
    draw = ImageDraw.Draw(img)

    # Draw the text
    draw.text((10,10), content, fill='black', font=font)

    # Find the position of the text to highlight
    start_index = content.find(text_to_highlight)
    if start_index != -1:
        # Create a dummy draw to measure the position of the highlight
        highlight_bbox = dummy_draw.textbbox((0, 0), content[:start_index], font=font)
        highlight_x = highlight_bbox[2] + 10

        highlight_text_bbox = dummy_draw.textbbox((0, 0), text_to_highlight, font=font)
        highlight_width = highlight_text_bbox[2]
        highlight_height = highlight_text_bbox[3]

        # Draw the highlight
        draw.rectangle(
            (highlight_x, 10, highlight_x + highlight_width, 10 + highlight_height),
            fill='yellow'
        )
        # Redraw the text on top of the highlight
        draw.text((10,10), content, fill='black', font=font)

    output_image_path = f"/tmp/highlighted_text.png"
    img.save(output_image_path)
    return [output_image_path]
