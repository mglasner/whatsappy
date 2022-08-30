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
CLIENT = Client(WHATSAPP_TOKEN, PHONE_NUMBER_ID)


def test_interactive_button_message():
    """Base case for interactive button message."""
    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=["title1", "title2"],
        body_text="This is the test body text",
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


def test_interactive_button_message_with_text_header():
    """Interactive button message with text header."""
    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=["title1", "title2"],
        body_text="This is the test body text",
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


def test_interactive_button_message_with_image_header():
    """Interactive button message with image header."""
    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=["title1", "title2"],
        body_text="This is the test body text with image header",
        header={
            "type": "image",
            "image": {"link": "https://picsum.photos/300/200"},
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


def test_interactive_button_message_with_document_header():
    """Interactive button message with document header."""
    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=["title1", "title2"],
        body_text="This is the test body text with document header",
        header={
            "type": "document",
            "document": {
                "link": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            },
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


def test_interactive_button_message_with_document_with_filename_header():
    """Interactive button message with document with filename header."""
    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=["title1", "title2"],
        body_text="This is the test body text with document header with filename",
        header={
            "type": "document",
            "document": {
                "link": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                "filename": "dumy_document.pdf",
            },
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


def test_interactive_button_message_with_footer():
    """Interactive button message with footer."""
    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=["title1", "title2"],
        body_text="This is the test body text with footer",
        footer={
            "text": "This is the footer text",
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


def test_interactive_button_message_with_header_and_footer():
    """Interactive button message with header and footer."""
    response = CLIENT.interactive_button_message(
        phone_number=TO,
        titles=["title1", "title2"],
        body_text="This is the test body text with header and footer",
        footer={
            "text": "This is the footer text",
        },
        header={
            "type": "image",
            "image": {"link": "https://picsum.photos/300/200"},
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
