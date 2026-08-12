from services.llm_service import summarize_text
from unittest.mock import MagicMock
def test_summarize_text_returns_model_content():
    fake_client = MagicMock()
    fake_response = MagicMock()
    fake_response.choices[0].message.content = "A concise manuscript summary."
    fake_client.chat.completions.create.return_value = fake_response

    result = summarize_text(
        ai_client=fake_client,
        deployment="test-deployment",
        text="A scientist is stranded on Mars.",
    )
    assert result == "A concise manuscript summary."