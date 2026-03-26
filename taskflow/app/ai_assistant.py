import anthropic
import os

def analyze_log(log_text):
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a DevOps expert assistant.
A developer has pasted the following error log or issue:

{log_text}

Please:
1. Explain what this error means in simple terms
2. Tell exactly what is causing it
3. Give clear steps to fix it

Keep your response practical and beginner friendly."""
            }
        ]
    )

    return message.content[0].text