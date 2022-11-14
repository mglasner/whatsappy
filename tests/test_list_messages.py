"""Module for testing list messages."""
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
SECTIONS = [
    (
        "Section1",
        [
            ("S1-Option1", "S1O1 description"),
            ("S1-Option2", "S1O2 description"),
        ],
    ),
    (
        "Section2",
        [
            ("S2-Option1", "S2O1 description"),
            ("S2-Option2", "S2O2 description"),
        ],
    ),
]
BUTTON_TEXT = "button text"
BODY_TEXT = "This is the body text"
TEXT_HEADER = {"type": "text", "text": "This is the header text"}
FOOTER = {"text": "This is the footer text"}


def test_interactive_list_message() -> None:
    """Base case for interactive list message."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.interactive_list_message(
        phone_number=TO,
        list_sections=SECTIONS,
        button_text=BUTTON_TEXT,
        body_text=BODY_TEXT,
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


def test_interactive_list_message_with_text_header() -> None:
    """Interactive list message with text header."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.interactive_list_message(
        phone_number=TO,
        list_sections=SECTIONS,
        button_text=BUTTON_TEXT,
        body_text=BODY_TEXT,
        header=TEXT_HEADER,
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


def test_interactive_list_message_with_footer() -> None:
    """Interactive list message with footer."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.interactive_list_message(
        phone_number=TO,
        list_sections=SECTIONS,
        button_text=BUTTON_TEXT,
        body_text=BODY_TEXT,
        footer=FOOTER,
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


def test_interactive_list_message_with_header_and_footer() -> None:
    """Interactive list message with header and footer."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.interactive_list_message(
        phone_number=TO,
        list_sections=SECTIONS,
        button_text=BUTTON_TEXT,
        body_text=BODY_TEXT,
        footer=FOOTER,
        header=TEXT_HEADER,
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
