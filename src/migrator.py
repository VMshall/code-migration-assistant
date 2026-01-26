import os
import re
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def migrate_code(source_code: str, from_framework: str, to_framework: str, notes: str = "") -> dict:
    prompt = f"""You are an expert code migration engineer.

Migrate this code from {from_framework} to {to_framework}.
{f'Additional context: {notes}' if notes else ''}

Source code:
```
{source_code[:5000]}
```

Respond ONLY with valid JSON:
{{
  "migrated_code": "string — complete migrated code, ready to run",
  "changes": [
    {{
      "description": "string — what changed",
      "reason": "string — why this change was needed",
      "breaking": true/false
    }}
  ],
  "breaking_changes": ["string — changes that require additional manual work"],
  "warnings": ["string — potential issues to watch for"],
  "confidence": "high|medium|low",
  "confidence_reason": "string — why confidence is at this level"
}}

Produce complete, working code. Note all breaking changes explicitly."""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    return json.loads(raw)
