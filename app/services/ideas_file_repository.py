from bs4 import BeautifulSoup

from typing import Optional

from app.core.settings import settings
from app.services.ideas_repository import IdeasRepository
from app.schemas.idea import Idea
from app.schemas.idea_create import IdeaCreate
from app.schemas.idea_update import IdeaUpdate

class IdeasFileRepository(IdeasRepository):
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
    
    def _read_file(self) -> str:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            md_file = file.read()
        return md_file
    
    def _write_to_file(self, soup: BeautifulSoup):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(soup.prettify(formatter=None))
    
    def _change_file(self, ideas):
        soup = BeautifulSoup(self._read_file(), 'html.parser')
        table_body = soup.find('tbody')
        new_tbody = soup.new_tag('tbody')

        id = 1
        for row in ideas:
            new_tr = soup.new_tag('tr')
            for field in ("id", "name", "short_description", "long_description"):
                new_td = soup.new_tag('td')
                if field == "id":
                    new_td.append(str(id))
                    id = id + 1
                else:
                    new_td.append(getattr(row, field))
                new_tr.append(new_td)
            new_tbody.append(new_tr)
        table_body.replace_with(new_tbody)

        self._write_to_file(soup)

    def get_idea(self, id: str) -> Optional[Idea]:
        for idea in self.get_ideas():
            if idea.id.strip() == id:
                return idea
        return None
    
    def get_ideas(self) -> list[Idea]:
        if self._ideas is None:
            self._ideas = self._load()
        return self._ideas
    
    def add_idea(self, new_idea: IdeaCreate) -> Optional[Idea]:
        ideas = self.get_ideas()

        idea_id = max(int(idea.id.strip()) for idea in ideas) + 1
        idea = Idea(id=str(idea_id),
                        name=new_idea.name,
                        short_description=new_idea.short_description,
                        long_description=new_idea.long_description)

        ideas.append(idea)
        self._change_file(ideas)

        return idea
    
    def update_idea(self, id: str, updated_idea: IdeaUpdate) -> Optional[Idea]:
        ideas = self.get_ideas()
        idea = self.get_idea(id)

        if updated_idea.name is not None:
            idea.name = updated_idea.name
        if updated_idea.short_description is not None:
            idea.short_description = updated_idea.short_description
        if updated_idea.long_description is not None:
            idea.long_description = updated_idea.long_description

        self._change_file(ideas)

        return idea
    
    def delete_idea(self, id: str) -> Optional[Idea]:
        ideas = self.get_ideas()
        idea = self.get_idea(id)

        deleted_idea = idea
        if deleted_idea:
            ideas.remove(idea)
            self._change_file(ideas)

        return deleted_idea