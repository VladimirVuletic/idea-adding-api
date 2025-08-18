from bs4 import BeautifulSoup

from app.core.settings import settings
from app.schemas.idea import Idea


class IdeasFile:
    file_path: str
    md_file: str
    ideas: list[Idea]

    def __init__(self, file_path: str = None):
        self.file_path = file_path if file_path else settings.REPO_PATH + settings.FILE_NAME
        self.read_file()
        self.ideas = []
        self.load_ideas()
        

    def read_file(self) -> str:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.md_file = file.read()

    def write_to_file(self, soup: BeautifulSoup):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(soup.prettify(formatter=None))

    def load_ideas(self) -> list[Idea]:
        soup = BeautifulSoup(self.md_file, 'html.parser')
        table_body = soup.find('tbody')
        table_rows = table_body.find_all('tr')

        for row in table_rows:
            idea = Idea(id=row.find_all('td')[0].decode_contents(),
                            name=row.find_all('td')[1].decode_contents(),
                            short_description=row.find_all('td')[2].decode_contents(),
                            long_description=row.find_all('td')[3].decode_contents())
            self.ideas.append(idea)

# Simple tests
ideas_file = IdeasFile()
print(ideas_file.file_path)
print(ideas_file.md_file)
print(ideas_file.ideas)