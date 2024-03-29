"""Module for testing text messages."""
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent))

from src.whatsappy.client import Client  # noqa

load_dotenv()
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
TO = os.getenv("TO")

if WHATSAPP_TOKEN is None:
    raise ValueError("WHATSAPP_TOKEN enviroment variable not found")

if PHONE_NUMBER_ID is None:
    raise ValueError("PHONE_NUMBER_ID enviroment variable not found")

CLIENT = Client(WHATSAPP_TOKEN, int(PHONE_NUMBER_ID))


def test_text_message() -> None:
    """Base case for text message."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.text_message(phone_number=TO, body="Test string")
    content = json.loads(response.content)
    assert "contacts" in content
    assert "messages" in content
    assert "messaging_product" in content
    assert "error" not in content
    assert content["messaging_product"] == "whatsapp"
    assert content["contacts"][0]["input"] == TO
    assert content["contacts"][0]["wa_id"] == TO
    assert response.status_code == 200


def test_text_message_with_preview_url() -> None:
    """Text message with preview url."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.text_message(
        phone_number=TO,
        body="You should see the preview url\nhttps://www.google.com",
        preview_url=True,
    )
    content = json.loads(response.content)
    assert "contacts" in content
    assert "messages" in content
    assert "messaging_product" in content
    assert "error" not in content
    assert content["messaging_product"] == "whatsapp"
    assert content["contacts"][0]["input"] == TO
    assert content["contacts"][0]["wa_id"] == TO
    assert response.status_code == 200


def test_text_message_without_preview_url() -> None:
    """Text message without preview url."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.text_message(
        phone_number=TO,
        body="You shouldn't see the preview url\nhttps://www.google.com",
    )
    content = json.loads(response.content)
    assert "contacts" in content
    assert "messages" in content
    assert "messaging_product" in content
    assert "error" not in content
    assert content["messaging_product"] == "whatsapp"
    assert content["contacts"][0]["input"] == TO
    assert content["contacts"][0]["wa_id"] == TO
    assert response.status_code == 200


def test_text_message_with_empty_body() -> None:
    """Text message with empty body."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.text_message(phone_number=TO, body="")
    content = json.loads(response.content)
    assert "contacts" not in content
    assert "messages" not in content
    assert "messaging_product" not in content
    assert "error" in content
    assert (
        content["error"]["message"] == "(#100) The parameter text['body'] is required."
    )
    assert content["error"]["type"] == "OAuthException"
    assert content["error"]["code"] == 100
    assert response.status_code == 400
