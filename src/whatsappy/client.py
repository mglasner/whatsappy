"""Client Module."""
import uuid
from typing import Any

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.models import Response


class Client:
    """A client to connect WhatsApp Business Cloud API."""

    def __init__(
        self, token: str, phone_number_id: int, api_version: str = "v15.0"
    ) -> None:
        """Initialize Client objetc.

        Reference: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages

        Args:
            token (str): WhatsApp Business Cloud API Token given by Meta.
            phone_number_id (str): Phone number id given by Meta.
            api_version (str, optional): Meta api version. Defaults to "v15.0".
        """
        self.token: str = token
        self.phone_number_id: int = phone_number_id
        self.url: str = f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages?access_token={token}"
        self.headers: dict = {"Content-Type": "application/json"}
        self.message: dict = {
            "messaging_product": "whatsapp",
        }

    def _config_and_post(self, _type: str, _to: str) -> Response:
        # sourcery skip: class-extract-method
        self.message["type"] = _type
        self.message["to"] = _to
        return self._post()

    def _post(self) -> Response:
        request_session = requests.Session()
        retries = Retry(
            total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )
        request_session.mount("", HTTPAdapter(max_retries=retries))
        return request_session.post(self.url, headers=self.headers, json=self.message)

    def mark_as_read(self, message_id: str) -> Response:
        """Mark messages as read.

        https://developers.facebook.com/docs/whatsapp/cloud-api/guides/mark-message-as-read

        Args:
            message_id (str): message id

        Returns:
            requests.models.Response: Object which contains a server's response
                to an HTTP request.
        """
        self.message["status"] = "read"
        self.message["message_id"] = message_id
        return self._post()

    def text_message(
        self, phone_number: str, body: str, preview_url: bool = False
    ) -> Response:
        """Send text messages.

        Args:
            phone_number (str): WhatsApp ID or phone number for the person you
                want to send a message to.
            body (str): The text of the text message.
            preview_url (bool, optional): Include a preview box with more
                information about the link. Defaults to False.

        Returns:
            requests.models.Response: Object which contains a server's response
                to an HTTP request.
        """
        self.message["text"] = {"body": body, "preview_url": preview_url}
        return self._config_and_post("text", phone_number)

    def interactive_button_message(
        self,
        phone_number: str,
        titles: list,
        body_text: str,
        header: dict | None = None,
        footer: dict | None = None,
    ) -> Response:
        """Send interactive button messages.

        Args:
            phone_number (str): WhatsApp ID or phone number for the person you
                want to send a message to.
            titles (list): List with the title text for every button (up to 3).
            body_text (str): Text for the body of the message.
            header(dict, optional): header Meta object:
                header = {
                    type: document, image, text, video,
                    if document or if image or if video): {
                        link: url for the document,
                        filename: optional, name for the file
                    },
                    text (if text): text for the header
                },
            footer_text (str, optional): Text for the footer of the message. Defaults to None.

        Returns:
            requests.models.Response: Object which contains a server's response
                to an HTTP request.
        """
        buttons = []
        for title in titles:
            button = {
                "type": "reply",
                "reply": {"id": str(uuid.uuid4()), "title": title},
            }
            buttons.append(button)

        interactive = {
            "type": "button",
            "action": {"buttons": buttons},
            "body": {"text": body_text},
            "header": header,
            "footer": footer,
        }

        self.message["interactive"] = interactive
        return self._config_and_post("interactive", phone_number)

    def interactive_list_message(
        self,
        phone_number: str,
        list_sections: list[tuple[str, list[tuple[str, str]]]],
        button_text: str,
        body_text: str,
        header: dict | None = None,
        footer: dict | None = None,
    ) -> Response:
        """Send interactive list messages.

        Args:
            phone_number (str): _description_
            list_sections (list[tuple[str, list[tuple[str, str]]]]): Sections with list of options.
                example for 1 section:
                    [
                        (
                            "Section 1 title",
                            [
                                ("Option 1 title", "Option 1 description"),
                                ("Option 2 title", "Option 2 description"),
                                ("Option 3 title", "Option 3 description"),
                            ]
                        ),
                    ]
            button_text (str): Text of the button for displaying the options.
            body_text (str): Text for the body of the message.
            header(dict, optional): header Meta object:
                header = {
                    type: document, image, text, video,
                    if document or if image or if video): {
                        link: url for the document,
                        filename: optional, name for the file
                    },
                    text (if text): text for the header
                },
            footer_text (str, optional): Text for the footer of the message. Defaults to None.

        Returns:
            requests.models.Response: _description_
        """
        sections = []
        for section_title, section_rows in list_sections:
            section: dict[str, Any] = {"title": section_title, "rows": []}
            for title, description in section_rows:
                section["rows"].append(
                    {
                        "id": str(uuid.uuid4()),
                        "title": title,
                        "description": description,
                    }
                )
            sections.append(section)

        interactive = {
            "type": "list",
            "action": {"button": button_text, "sections": sections},
            "body": {"text": body_text},
            "header": header,
            "footer": footer,
        }

        self.message["interactive"] = interactive
        return self._config_and_post("interactive", phone_number)

    def template_message(
        self,
        phone_number: str,
        template_name: str,
        language: str,
        components: dict | None = None,
    ) -> Response:
        """Send template messages.

        Components support only for type header and body.

        Args:
            phone_number (str): WhatsApp ID or phone number for the person you
                want to send a message to.
            template_name (str): Name of the template.
            language (str): Contains a language object.
                Specifies the language the template may be rendered in.
            components (dict): Dictionary of components.
                Read documentation for details.
                type options are: header and body.
                Defaults to None.

        Returns:
            requests.models.Response: Object which contains a server's response
                to an HTTP request.
        """
        template = {
            "name": template_name,
            "language": {"code": language},
            "components": components,
        }

        self.message["template"] = template
        return self._config_and_post("template", phone_number)

    def media_message(
        self,
        phone_number: str,
        media_type: str,
        link: str,
        caption: str | None = None,
        filename: str | None = None,
    ) -> Response:
        """Send media messages.

        Args:
            phone_number (str): WhatsApp ID or phone number for the person you
                want to send a message to.
            media_type (str): Media type. Options: image, audio or document.
            link (str): Url for the media.
            caption (str, optional): Text message with the media file.
                Defaults to None.
            filename (str, optional): Filename for media file.
                Defaults to None.

        Returns:
            requests.models.Response: _description_
        """
        media = {"link": link}
        if caption is not None:
            media["caption"] = caption

        if filename is not None:
            media["filename"] = filename

        self.message[media_type] = media
        return self._config_and_post(media_type, phone_number)
