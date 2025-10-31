def parse_txt(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def parse_md(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def parse_html(file_path):
    with open(file_path, 'r') as f:
        return f.read()
