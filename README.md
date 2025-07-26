https://fastapi.tiangolo.com/#example

## Create it

Create a file main.py with:

```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

## Run it

Run the server with: `fastapi dev main.py`


## Check it

Open your browser at http://127.0.0.1:8000/items/5?q=somequery.

You will see the JSON response as:

`{"item_id": 5, "q": "somequery"}`

You already created an API that:
- Receives HTTP requests in the paths / and /items/{item_id}.
- Both paths take GET operations (also known as HTTP methods).
- The path /items/{item_id} has a path parameter item_id that should be an int.
- The path /items/{item_id} has an optional str query parameter q.

### TESTING THE TABLES

| Name    | Age | City     |
|---------|-----|----------|
| Alice   | 30  | London   |
| Bob     | 25  | Paris    |
| Charlie | 35  | New York |


<table>
  <thead>
    <tr><th>Name</th><th>Age</th><th>City</th></tr>
  </thead>
  <tbody>
    <tr><td>Alice</td><td>30</td><td>London</td></tr>
    <tr><td>Bob</td><td>25</td><td>Paris</td></tr>
    <tr><td>Charlie</td><td>35</td><td>New York</td></tr>
  </tbody>
</table>
