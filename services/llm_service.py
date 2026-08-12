from typing import Any


def summarize_text(
    ai_client: Any,
    deployment: str,
    text: str,
) -> str:
    response = ai_client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an editorial assistant at a publishing house. "
                    "Be concise."
                ),
            },
            {
                "role": "user",
                "content": f"Summarize in two sentences:\n\n{text}",
            },
        ],
    )

    summary = response.choices[0].message.content

    if not summary:
        raise ValueError("The model returned an empty summary")

    return summary