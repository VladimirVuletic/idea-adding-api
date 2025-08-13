from bs4 import BeautifulSoup

import subprocess
from typing import Optional

from app.schemas.idea import Idea
from app.core.settings import settings


def get_table() -> list[Idea]:
    md_file = read_file()

    soup = BeautifulSoup(md_file, 'html.parser')
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

def read_file():
    file_path = settings.REPO_PATH + settings.FILE_NAME

    with open(file_path, 'r', encoding='utf-8') as file:
        md_file = file.read()

    return md_file

def find_idea_by_id(id: str, ideas: list[Idea]) -> Optional[Idea]:
    for idea in ideas:
        if idea.id.strip() == id:
            return idea
    return None

def write_to_file(soup: BeautifulSoup):
    file_path = settings.REPO_PATH + settings.FILE_NAME

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify(formatter=None))

def change_file(ideas_table):
    md_file = read_file()

    soup = BeautifulSoup(md_file, 'html.parser')
    table_body = soup.find('tbody')
    new_tbody = soup.new_tag('tbody')

    id = 1
    for row in ideas_table:
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

    write_to_file(soup)

def run_cmd(cmd, cwd):
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout

def push_changes(commit_message):
    repo_path = settings.REPO_PATH

    output = []
    for git_cmd in [
        ['git', 'add', '.'],
        ['git', 'commit', '-m', commit_message],
        ['git', 'push']
    ]:
        output.append(run_cmd(git_cmd, repo_path))

    return output