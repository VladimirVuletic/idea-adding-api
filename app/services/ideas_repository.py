from bs4 import BeautifulSoup

from typing import Optional

from app.schemas.idea import Idea
from app.core.settings import settings


class IdeasRepository():
    def __init__(self, file_path: str = None):
        self.file_path = file_path if file_path else settings.REPO_PATH + settings.FILE_NAME
        self._ideas: Optional[list[Idea]] = None

    def _load(self):
        soup = BeautifulSoup(self._read_file(), 'html.parser')
        table_body = soup.find('tbody')
        table_rows = table_body.find_all('tr')

        ideas = []
        for row in table_rows:
            idea = Idea(id=row.find_all('td')[0].decode_contents(),
                            name=row.find_all('td')[1].decode_contents(),
                            short_description=row.find_all('td')[2].decode_contents(),
                            long_description=row.find_all('td')[3].decode_contents())
            ideas.append(idea)
        return ideas
    
    def _read_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            md_file = file.read()
        return md_file

    def get_idea(self, id: str) -> Optional[Idea]:
        for idea in self.get_ideas():
            if idea.id.strip() == id:
                return idea
        return None
    
    def get_ideas(self) -> list[Idea]:
        if self._ideas is None:
            self._ideas = self._load()
        return self._ideas


# We should have file repo and db repo btw