# code-migration-assistant

AI code migration assistant — migrate between frameworks/versions with detailed change log and breaking change warnings

## Setup
```bash
cp .env.example .env  # add ANTHROPIC_API_KEY
pip install -r requirements.txt
uvicorn src.api:app --reload
```
