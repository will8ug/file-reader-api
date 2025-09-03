# File Reader API

A simple Python FastAPI application that reads local files and exposes a REST API to return file content and metadata.

## Setup

### Prerequisites

- Python 3.8 or higher
- uv package manager

### Installation

1. Install dependencies using uv:
```bash
uv sync
```

2. Run the application:
```bash
uv run python run.py
# OR
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Usage

### Get All Prompts (Metadata Only)

```bash
curl http://localhost:8000/api/prompt-templates
```

Response:
```json
{
  "prompts": [
    {
      "name": "hello",
      "code": 1,
      "scope": "Word",
      "params": {
        "mandatory": ["name"],
        "optional": ["original_content"]
      },
      "file": "hello.txt"
    }
  ]
}
```

### Get Specific Prompt (With Content)

```bash
curl "http://localhost:8000/api/prompt-templates?code=1"
```

Response:
```json
{
  "prompt": {
    "name": "hello",
    "code": 1,
    "scope": "Word",
    "params": {
      "mandatory": ["name"],
      "optional": ["original_content"]
    },
    "content": "Hello, {name}! Welcome!\n\n{original_content}"
  }
}
```

### Other Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)

## Development

### Running Tests

```bash
uv run pytest tests/ -v
```

### 📚 More UV Commands

```bash
# Add to main dependencies
uv add package-name

# Add to dev dependencies
uv add --dev package-name

# Check what's installed
uv pip list

# Update dependencies
uv sync --upgrade

# Remove dependencies
uv remove package-name

# Show dependency tree
uv tree
```
