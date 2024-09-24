from pypdf import PdfReader


class File:

    def __init__(self, path):
        self.path = path

    def content(self):
        if self.path.name.endswith('.pdf'):
            reader = PdfReader(self.path.resolve())
            content = ''.join(
                page.extract_text()
                for page in reader.pages
            )
        else:
            with open(self.path.resolve(), 'r') as f:
                content = f.read()
        return content
