def parse_ideas(markdown: str):
    lines = markdown.splitlines()
    # 1) Find where the table header (“| Project Name | …”) sits
    for i, line in enumerate(lines):
        if line.strip().startswith("| Project Name"):
            header_idx = i
            break
    else:
        return []  # no table found

    # 2) Skip the header and the separator (`|---|---|---|`)
    data_lines = lines[header_idx+2:]
    ideas = []
    for row in data_lines:
        if not row.strip().startswith("|"):
            break
        # strip leading/trailing '|' and split cells
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        # guard against empty rows
        if len(cells) < 3 or all(not c for c in cells):
            continue
        ideas.append({
            "Project Name":       cells[0],
            "Short Description":  cells[1],
            "Long Description":   cells[2],
        })
    return ideas

# --- usage ---
file_path = r"C:/Python projects/future-projects/README.md"
with open(file_path, 'r', encoding='utf-8') as f:
    md = f.read()

idea_list = parse_ideas(md)
print(idea_list)
