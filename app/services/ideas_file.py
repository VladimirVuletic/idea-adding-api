from bs4 import BeautifulSoup

from app.core.settings import settings
from app.schemas.idea import Idea

from fastapi import FastAPI
from app.schemas.idea import Idea
from app.schemas.idea_create import IdeaCreate

app = FastAPI()


class IdeasFile:
    file_path: str
    md_file: str = None
    ideas: list[Idea] = []

    def __init__(self, file_path: str = None):
        self.file_path = file_path if file_path else settings.REPO_PATH + settings.FILE_NAME
        self.read_file()
        self.load_ideas()

    def add_idea(self, idea: IdeaCreate):
        new_idea_id = max(int(idea.id.strip()) for idea in self.ideas) + 1
        new_idea = Idea(id=str(new_idea_id),
                    name=idea.name,
                    short_description=idea.short_description,
                    long_description=idea.long_description)

        self.ideas.append(new_idea)
        self.change_file(self.ideas)

        return new_idea

    def change_file(self, ideas: list[Idea]):
        soup = BeautifulSoup(self.md_file, 'html.parser')
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

        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(soup.prettify(formatter=None))
        
    def read_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.md_file = file.read()
    

    def load_ideas(self):
        soup = BeautifulSoup(self.md_file, 'html.parser')
        table_body = soup.find('tbody')
        table_rows = table_body.find_all('tr')

        for row in table_rows:
            idea = Idea(id=row.find_all('td')[0].decode_contents(),
                            name=row.find_all('td')[1].decode_contents(),
                            short_description=row.find_all('td')[2].decode_contents(),
                            long_description=row.find_all('td')[3].decode_contents())
            self.ideas.append(idea)

    def get_ideas(self) -> list[Idea]:
        return self.ideas

ideas_file = IdeasFile()


@app.post('/ideas', response_model=Idea)
def create_idea(new_idea: IdeaCreate, ideas: list[Idea] = ideas_file.get_ideas()) -> Idea:

    added_idea = ideas_file.add_idea(new_idea)

    return added_idea
