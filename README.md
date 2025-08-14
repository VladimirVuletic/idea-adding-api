## Installation

1. **Install dependencies:**
`pip install -r requirements.txt`
2. **Create a .env file in the project root with the following variables:**
```
REPO_PATH=...       # Path to your repo root
FILE_NAME=...       # Markdown file with the ideas table
```

## To-do
1. Add integration tests for every endpoint
   - first_n as a float (1.0), and first_n as a negative float (-1.0) — Should not truncate: expect 422 or 400 per your API contract.
   - Path param with special characters (URL encoded) and multi-byte unicode id to ensure normalization/strip logic
2. Group integration tests by endpoint/behavior
3. Add all unit tests
4. Introduce a DB
5. Authentication
6. Logging?
7. Rate limiting?
8. Async?
9. Containerization?