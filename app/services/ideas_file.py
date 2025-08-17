from bs4 import BeautifulSoup

from app.core.settings import settings

class IdeasFile:
    file_path: str

    def __init__(self, file_path: str = None):
        self.file_path = file_path if file_path else settings.REPO_PATH + settings.FILE_NAME

    def read_file(self): ## Add typing
        with open(self.file_path, 'r', encoding='utf-8') as file:
            md_file = file.read()

        return md_file
    
    def write_to_file(self, soup: BeautifulSoup):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(soup.prettify(formatter=None))