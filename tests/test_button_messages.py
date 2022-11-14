"""Module for testing button messages."""
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
TITLES = ["title1", "title2"]
BODY = "This is the test body text"
FOOTER = {"text": "This is the footer text"}
DOCUMENT_LINK = (
    "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
)
IMAGE_LINK = "https://picsum.photos/300/200"


def test_interactive_button_message() -> None:
    """Base case for interactive button message."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=TITLES,
        body_text=BODY,
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


def test_interactive_button_message_with_text_header() -> None:
    """Interactive button message with text header."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=TITLES,
        body_text=BODY,
        header={"type": "text", "text": "This is the header text"},
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


def test_interactive_button_message_with_image_header() -> None:
    """Interactive button message with image header."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=TITLES,
        body_text=f"{BODY} with image header",
        header={"type": "image", "image": {"link": IMAGE_LINK}},
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


def test_interactive_button_message_with_document_header() -> None:
    """Interactive button message with document header."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=TITLES,
        body_text=f"{BODY}  with document header",
        header={"type": "document", "document": {"link": DOCUMENT_LINK}},
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


def test_interactive_button_message_with_document_with_filename_header() -> None:
    """Interactive button message with document with filename header."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=TITLES,
        body_text=f"{BODY}  with document header with filename",
        header={
            "type": "document",
            "document": {"link": DOCUMENT_LINK, "filename": "dumy_document.pdf"},
        },
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


def test_interactive_button_message_with_footer() -> None:
    """Interactive button message with footer."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=TITLES,
        body_text=f"{BODY}  with footer",
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


def test_interactive_button_message_with_header_and_footer() -> None:
    """Interactive button message with header and footer."""
    if TO is None:
        raise ValueError("TO enviroment variable not found")

    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=TITLES,
        body_text=f"{BODY}  with header and footer",
        footer=FOOTER,
        header={"type": "image", "image": {"link": IMAGE_LINK}},
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
