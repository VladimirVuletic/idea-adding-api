from bs4 import BeautifulSoup

def get_table():
    file_path = r"C:/Python projects/future-projects/README.md"

    with open(file_path, 'r', encoding='utf-8') as file:
        md_file = file.read()

    soup = BeautifulSoup(md_file, 'html.parser')
    table_body = soup.find('tbody')
    table_rows = table_body.find_all('tr')

    json_table = []
    for row in table_rows:
        json_row = {
            "ID": row.find_all('td')[0].decode_contents(),
            "Project name": row.find_all('td')[1].decode_contents(),
            "Short description": row.find_all('td')[2].decode_contents(),
            "Long description": row.find_all('td')[3].decode_contents()
        }
        json_table.append(json_row)

    return json_table

def change_file(json_table):
    file_path = r"C:/Python projects/future-projects/README.md"
    with open(file_path, 'r', encoding='utf-8') as file:
        md_file = file.read()
    soup = BeautifulSoup(md_file, 'html.parser')

    print(soup)

    table_body = soup.find('tbody')

    new_tbody = soup.new_tag('tbody')

    id = 1
    for row in json_table:
        new_tr = soup.new_tag('tr')
        for field in ("ID", "Project name", "Short description", "Long description"):
            new_td = soup.new_tag('td')
            if field == "ID":
                new_td.append(str(id))
                id = id + 1
            else:
                new_td.append(row[field])
            new_tr.append(new_td)
        new_tbody.append(new_tr)
    table_body.replace_with(new_tbody)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify(formatter=None))

# GET, POST, PUT, DELETE


def get_idea(id):
    json_table = get_table()

    for idea in json_table:
        if idea['ID'] == id:
            return {'result': idea}
        
def get_ideas(first_n: int = None): # default value of none
    json_table = get_table()

    if first_n:
        return json_table[:first_n]
    else:
        return json_table


def create_idea(idea: dict):
    json_table = get_table()
    new_idea_id = max(int(idea['ID']) for idea in json_table) + 1

    new_idea = {
        'ID': str(new_idea_id),
        'Project name': idea['Project name'],
        'Short description': idea['Short description'],
        'Long description': idea['Long description']
    }

    json_table.append(new_idea)

    change_file(json_table)

    return new_idea

# print(get_table())
change_file(get_table())
# print(get_table())