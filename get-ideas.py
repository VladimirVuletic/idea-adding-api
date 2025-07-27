from bs4 import BeautifulSoup

file_path = r"C:/Python projects/future-projects/README.md"

with open(file_path, 'r', encoding='utf-8') as file:
    md_file = file.read()

soup = BeautifulSoup(md_file, 'html.parser')
table_body = soup.find('tbody')
table_rows = table_body.find_all('tr')

json_table = []
for row in table_rows:
    json_row = {
        "ID": row.find_all('td')[0].decode_contents()  ,
        "Project name": row.find_all('td')[1].decode_contents()  ,
        "Short description": row.find_all('td')[2].decode_contents()  ,
        "Long description": row.find_all('td')[3].decode_contents()
    }
    json_table.append(json_row)

print(json_table)